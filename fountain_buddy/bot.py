"""Discord: post each sighting with buttons, record the human's answer as a label.

Buttons are discord.py DynamicItems keyed by custom_id ("fb:<action>:<visit>[:<label>]"),
so posts keep working across restarts. A typed reply to a post works too. Only answers in
the configured channel count, and only humans (not bots or webhooks) can label.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import json
import logging
import re
from contextlib import closing
from pathlib import Path

import discord

from fountain_buddy import db, species

log = logging.getLogger(__name__)

TOP_BUTTONS = 3
DROPDOWN = [*species.SPECIES, species.SQUIRREL]  # <= 25 options
SKIP_WORDS = ("skip", "poor", "blur", "bad")

COLOR_OPEN = 0x5865F2
COLOR_DONE = 0x2ECC71
COLOR_SKIP = 0x95A5A6


# -- the database side -------------------------------------------------------------


def visit_state(store: Path, visit_id: int) -> dict:
    with closing(db.connect(store)) as conn:
        visit = conn.execute(
            "SELECT v.taken_at, v.camera, v.source, p.top_k FROM visits v "
            "JOIN predictions p ON p.id = (SELECT MAX(id) FROM predictions WHERE visit_id = v.id) "
            "WHERE v.id = ?",
            (visit_id,),
        ).fetchone()
        label = conn.execute(
            "SELECT label, labeled_by FROM current_labels WHERE visit_id = ?", (visit_id,)
        ).fetchone()
    return {
        "visit_id": visit_id,
        "taken_at": dt.datetime.fromisoformat(visit["taken_at"]),
        "source": visit["source"],
        "ranked": [tuple(x) for x in json.loads(visit["top_k"])],
        "label": label["label"] if label else None,
        "labeled_by": label["labeled_by"] if label else None,
    }


def add_label(store: Path, visit_id: int, label: str, who: str) -> None:
    with closing(db.connect(store)) as conn:
        conn.execute(
            "INSERT INTO labels (visit_id, label, source, labeled_at, labeled_by) "
            "VALUES (?, ?, 'discord', ?, ?)",
            (visit_id, label, dt.datetime.now().isoformat(timespec="seconds"), who),
        )
        conn.commit()


def parse_reply(text: str) -> str | None:
    """A typed answer: a known label, a skip word, or (title-cased) any other species."""
    text = " ".join(text.split())
    if not text:
        return None
    if any(w in text.lower().split() for w in SKIP_WORDS):
        return species.SKIP
    return species.canonical(text) or text.title()


# -- rendering ---------------------------------------------------------------------


def _when(state: dict) -> str:
    test = "TEST (not trained on) · " if state.get("source") == "test" else ""
    return f"{test}Tray Feeder · {state['taken_at']:%a %-I:%M:%S %p}"


def render(state: dict) -> tuple[discord.Embed, discord.ui.View]:
    visit_id, ranked = state["visit_id"], state["ranked"]
    guess, p = ranked[0]
    image = f"attachment://visit-{visit_id}.jpg"
    if state["label"] is None:
        title = f"{guess}?  ({p:.0%})" if guess in species.SPECIES else "Unclear photo. What is it?"
        others = ", ".join(f"{label} {q:.0%}" for label, q in ranked[1:4] if q >= 0.02)
        embed = discord.Embed(title=title, description=_when(state), color=COLOR_OPEN)
        if others:
            embed.add_field(name="Also possible", value=others, inline=False)
        embed.set_image(url=image)
        return embed, choices_view(visit_id, ranked)

    label = state["label"]
    right = label == guess
    verdict = "guessed right" if right else f"guessed {guess} ({p:.0%})"
    embed = discord.Embed(
        title=f"✅ {label}" if label != species.SKIP else "🗑️ Skipped",
        description=f"{_when(state)}\nLabeled by {state['labeled_by']} · model {verdict}",
        color=COLOR_SKIP if label == species.SKIP else COLOR_DONE,
    )
    embed.set_image(url=image)
    view = discord.ui.View(timeout=None)
    view.add_item(ChangeButton(visit_id))
    return embed, view


def choices_view(visit_id: int, ranked: list[tuple[str, float]]) -> discord.ui.View:
    view = discord.ui.View(timeout=None)
    top = [label for label, _ in ranked if label in species.SPECIES][:TOP_BUTTONS]
    for i, label in enumerate(top):
        style = discord.ButtonStyle.success if i == 0 else discord.ButtonStyle.secondary
        view.add_item(LabelButton(visit_id, label, style, row=0))
    view.add_item(OtherSelect(visit_id))
    view.add_item(LabelButton(visit_id, species.SKIP, discord.ButtonStyle.secondary, row=2))
    view.add_item(LabelButton(visit_id, species.NOT_A_BIRD, discord.ButtonStyle.secondary, row=2))
    return view


# -- components ----------------------------------------------------------------------


class LabelButton(
    discord.ui.DynamicItem[discord.ui.Button], template=r"fb:l:(?P<visit>\d+):(?P<label>.+)"
):
    def __init__(self, visit_id: int, label: str, style=discord.ButtonStyle.secondary, row=None):
        text = "Skip (bad photo)" if label == species.SKIP else label
        super().__init__(
            discord.ui.Button(
                label=text, style=style, row=row, custom_id=f"fb:l:{visit_id}:{label}"
            )
        )
        self.visit_id, self.label = visit_id, label

    @classmethod
    async def from_custom_id(cls, interaction, item, match: re.Match[str], /):
        return cls(int(match["visit"]), match["label"])

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.client.answer(interaction, self.visit_id, self.label)


class OtherSelect(discord.ui.DynamicItem[discord.ui.Select], template=r"fb:o:(?P<visit>\d+)"):
    def __init__(self, visit_id: int):
        super().__init__(
            discord.ui.Select(
                custom_id=f"fb:o:{visit_id}",
                placeholder="Something else…",
                options=[discord.SelectOption(label=label) for label in DROPDOWN],
                row=1,
            )
        )
        self.visit_id = visit_id

    @classmethod
    async def from_custom_id(cls, interaction, item, match: re.Match[str], /):
        return cls(int(match["visit"]))

    async def callback(self, interaction: discord.Interaction) -> None:
        values = interaction.data.get("values") or []
        if values:
            await interaction.client.answer(interaction, self.visit_id, values[0])


class ChangeButton(discord.ui.DynamicItem[discord.ui.Button], template=r"fb:c:(?P<visit>\d+)"):
    def __init__(self, visit_id: int):
        super().__init__(
            discord.ui.Button(
                label="Change", style=discord.ButtonStyle.secondary, custom_id=f"fb:c:{visit_id}"
            )
        )
        self.visit_id = visit_id

    @classmethod
    async def from_custom_id(cls, interaction, item, match: re.Match[str], /):
        return cls(int(match["visit"]))

    async def callback(self, interaction: discord.Interaction) -> None:
        bot: FeederBot = interaction.client
        state = visit_state(bot.store, self.visit_id)
        state["label"] = None  # show the choices again; the old label stands until replaced
        embed, view = render(state)
        await interaction.response.edit_message(embed=embed, view=view)


# -- the client ----------------------------------------------------------------------


class FeederBot(discord.Client):
    def __init__(self, store: Path, channel_id: int):
        intents = discord.Intents.default()
        intents.message_content = True  # typed replies
        super().__init__(intents=intents, allowed_mentions=discord.AllowedMentions.none())
        self.store, self.channel_id = store, channel_id
        self.ready = asyncio.Event()
        # Set by the service: returns the text for a `status` message.
        self.status_provider = None

    async def setup_hook(self) -> None:
        self.add_dynamic_items(LabelButton, OtherSelect, ChangeButton)

    async def on_ready(self) -> None:
        log.info("discord: logged in as %s", self.user)
        self.ready.set()

    async def channel(self) -> discord.TextChannel:
        return self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)

    async def post(self, visit_id: int, preview: Path) -> discord.Message:
        state = visit_state(self.store, visit_id)
        embed, view = render(state)
        file = discord.File(preview, filename=f"visit-{visit_id}.jpg")
        message = await (await self.channel()).send(embed=embed, view=view, file=file)
        with closing(db.connect(self.store)) as conn:
            conn.execute(
                "INSERT INTO posts (message_id, visit_id, channel_id, posted_at) "
                "VALUES (?, ?, ?, ?)",
                (message.id, visit_id, message.channel.id,
                 dt.datetime.now().isoformat(timespec="seconds")),
            )  # fmt: skip
            conn.commit()
        return message

    async def say(self, text: str) -> None:
        await (await self.channel()).send(text)

    async def answer(self, interaction: discord.Interaction, visit_id: int, label: str) -> None:
        if interaction.channel_id != self.channel_id or interaction.user.bot:
            await interaction.response.send_message("Not here.", ephemeral=True)
            return
        add_label(self.store, visit_id, label, interaction.user.display_name)
        log.info("visit %d labeled %r by %s", visit_id, label, interaction.user.display_name)
        embed, view = render(visit_state(self.store, visit_id))
        await interaction.response.edit_message(embed=embed, view=view)

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.webhook_id or message.channel.id != self.channel_id:
            return
        if message.reference is None:
            if message.content.strip().lower() in ("status", "!status") and self.status_provider:
                await message.reply(self.status_provider())
            return
        with closing(db.connect(self.store)) as conn:
            row = conn.execute(
                "SELECT visit_id FROM posts WHERE message_id = ?", (message.reference.message_id,)
            ).fetchone()
        label = parse_reply(message.content)
        if row is None or label is None:
            return
        visit_id = row[0]
        add_label(self.store, visit_id, label, message.author.display_name)
        log.info("visit %d labeled %r by %s (reply)", visit_id, label, message.author.display_name)
        await message.add_reaction("✅" if label in species.LABELS else "🆕")
        original = await message.channel.fetch_message(message.reference.message_id)
        embed, view = render(visit_state(self.store, visit_id))
        await original.edit(embed=embed, view=view)
