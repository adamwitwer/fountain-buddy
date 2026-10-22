# Fountain Buddy

A feeder camera that identifies its visitors and gets better at it from your answers.

1. The Reolink camera reports motion.
2. A burst of frames is checked by an object detector (YOLO) for birds.
3. The best crop is classified by a small model trained on top of a biology foundation
   model (BioCLIP 2), using every answer you have ever given.
4. Discord gets the photo with the top guesses as buttons.
5. You tap the right one (or Skip). That answer becomes training data; an unanswered
   post never does.
6. Answered sightings go on a public page, [adamwitwer.com/birds](https://adamwitwer.com/birds/),
   with the model's guess beside your answer.

Version 2 is a rebuild started in October 2026. The plan and its progress are in
[PLAN.md](PLAN.md); how to work on the code is in [AGENTS.md](AGENTS.md). Version 1 (two
cameras, a TensorFlow CNN, numbered text replies) is archived.

## Setup

Runs on an Apple Silicon Mac (Metal for inference). Needs [uv](https://docs.astral.sh/uv/).

```bash
uv sync                     # Python 3.13 venv in .venv with all dependencies
cp .env.example .env        # then fill it in; chmod 600 .env
git config core.hooksPath .githooks   # blocks commits containing secrets or data
uv run fountain-buddy check # camera login and settings sanity check
uv run pytest
```

Photos, the database and trained models live in `data/`, which git never tracks.

To run it as a service on the Mac: `launchd/install.sh` (see AGENTS.md, "Deploying").

## Is it running?

1. **In Discord, type `status` in #tray-feeder.** A reply means the service is up. It
   shows how long it has been running, when the camera last answered (⚠️ if more than
   15 minutes ago), today's counts, and the last bird. No birds but a ✅ camera just
   means a quiet tray.
2. **No reply?** On the Mini:
   `cd /Volumes/Envoy/apps/fountain-buddy && uv run fountain-buddy status`
   It shows launchd's view, the last start, recent warnings, and whether the camera
   answers on the network.
3. **Fix:** `launchd/install.sh` restarts it. Then look at the Mini's screen: a macOS
   permission dialog ("python3.13 would like to access…") pauses the service until you
   click Allow.
4. The bot also posts on its own when the camera has been unreachable for 15 minutes,
   and again when it comes back.

## Hardware

- Reolink RLC-810WA (4K, Wi-Fi) aimed at a safflower tray feeder.
- Mac mini (M4 Pro) that never sleeps.
- A Discord server with a bot that has Send Messages, Attach Files, Add Reactions and
  Read Message History in one channel.
