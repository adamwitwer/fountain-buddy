# AGENTS.md

Guidance for AI agents (Claude Code and others) working in this repo. This project is a
collaboration: agents are expected to offer opinions, push back and suggest improvements,
not just execute. Record that input in the log at the bottom.

## Project

A Reolink camera watches a safflower tray feeder. On motion, the service grabs a burst of
frames, finds the bird (YOLO), guesses the species (a small classifier on BioCLIP 2
features), and posts to Discord with the top guesses as buttons. Adam's answer is the
ground truth that the classifier retrains on. **An unanswered post is never a
confirmation and never trains anything.**

The rebuild plan, its decisions and phase checkboxes are in `PLAN.md`. Until the rebuild
ships, PLAN.md is the source of truth for scope; update it when a decision changes.

## Where we left off (2026-10-18)

- Phase 0: done. The old GitHub repo is now `fountain-buddy-legacy` (private, archived),
  and every leaked secret has been rotated or revoked. Channel renamed `#tray-feeder`.
- Phase 1: done. Fresh public repo, `.env` on the new key names, `check` passes.
- Next: Phase 2, rescuing the 3,636 human verifications from `data/legacy.db`.

## Commands

```bash
uv sync                          # .venv, Python 3.13
uv run fountain-buddy check      # settings + camera login
uv run pytest                    # run before every commit
uv run ruff check . && uv run ruff format --check .
git config core.hooksPath .githooks   # once per clone: the secrets/data guard
```

## Conventions

- **This repo is public, and the last one leaked every secret.** v1 committed launchd
  plists with secrets inline in `EnvironmentVariables` (`18cca1d`, 2025-08-03), which went
  unnoticed for 14 months. So:
  - Secrets live only in `.env` (mode 600), read at runtime. A launchd plist never
    contains a secret; only a `*.plist.example` template is tracked.
  - `scripts/hygiene.py` fails if the git index holds a forbidden path (.env, db, images,
    weights, plists, `data/`) or any file containing a `.env` value or a Discord token or
    webhook. It runs in `tests/test_hygiene.py` and the pre-commit hook. Don't weaken it
    to get a commit through; fix the commit.
  - Never print a secret to the terminal or a log. Check with `bool(settings().x)`.
  - Keep Tailscale addresses and other network details out of this repo. LAN addresses
    for the camera are fine.
- **Data lives in `data/`** (gitignored): `images/`, `fountain_buddy.db`, `models/`, and
  `legacy.db` (v1's database, read-only source for the import).
- **Human labels and model output are stored apart.** A prediction is never promoted to
  a label. Labels come only from a human action in Discord.
- **Species names are canonical** (`fountain_buddy/species.py`): title case, spaces. Map
  anything typed or imported through `species.canonical()`. `Skip` means "unusable
  photo": it trains the not-usable class but is never a sighting. The Discord dropdown
  holds at most 25 options.
- **Settings are read lazily** through `config.settings()`, never captured at import.
- **Python 3.13, uv-managed.** No TensorFlow. PyTorch on MPS.
- **Measure models on our own photos, split by time** (older to train, newer to test). A
  retrained model replaces the current one only if it scores at least as well.
- Run `pytest` before every commit. After a search-and-replace edit, grep to confirm it
  landed.

## The camera (Tray Feeder)

Reolink RLC-810WA at 192.168.50.249, 4K (3840×2160) on Wi-Fi, firmware v3.0.0.4348.
Learned from v1 and the 2026-10-18 probe:

- Built-in AI detects people, vehicles and dog/cat. **There is no bird class**, so
  camera AI alone can't trigger on birds; motion plus our own detector does.
- v1 polled `GetMdState`/`GetAiState` every second over HTTP and ended in an endless
  "please login first" loop (token invalidated, never re-acquired). Use push events
  (Baichuan, port 9000, via `reolink_aio`) and re-login on auth errors.
- HTTP `Snap` returns a full 4K JPEG (~0.8 MB). RTSP is on 554.
- Frames carry burned-in overlays: date/time top center, a Reolink watermark top left,
  "Tray Feeder" bottom right. The view is fisheye-ish.

## Legacy (v1)

v1 lives at `/Volumes/Envoy/apps/fountain-buddy-legacy` (local checkout, with NABirds and
the old training sets) and `github.com/adamwitwer/fountain-buddy-legacy` (private,
archived). Facts about its data that matter for the import:

- `data/legacy.db` has 7,884 visits (2025-06-28 to 2025-12-26). A row is human-verified
  when `confidence = 1.0`: 3,636 rows, 379 of them "Skip". Labels include strays like
  `Skiip`, `Blue_Jay` and `Unknown; Not A Bird`.
- Saved JPEGs have the YOLO box and label **drawn into them**. Cut training crops from
  inside the drawn box.
- `image_path` values are relative to v1's root (`bird_images/...`), now under
  `data/images/...`.
- Rows from Dec 2025 tagged `fountain` were taken by the Peanut Feeder camera (its
  overlay says so).
- v1's classifier agreed with Adam in 25 of 549 posts in Aug 2025. Don't use its
  `ai_species` column as anything but a baseline.

## Agent input log

Suggestions, concerns and opinions from agents, with their status. Newest first. Status
is one of: open / adopted / declined / done.

| Date | Input | Status |
|------|-------|--------|
| 2026-10-18 | Start a fresh public repo instead of rewriting v1's history. A force-push leaves the old commits reachable by SHA on GitHub, and rotating the secrets is the real fix anyway. v1 was renamed `fountain-buddy-legacy`, made private and archived. This repo took the name. | done |
| 2026-10-18 | Replace the TF CNN with frozen foundation-model features plus a small classifier trained on Adam's labels. The CNN was trained mostly on NABirds' professional photos and failed on the feeder camera. A small head retrains in seconds, so the model can learn after every few answers. BioCLIP 2 vs DINOv3 is decided by a bake-off on our data (Phase 3). | adopted |
| 2026-10-18 | Discord bot posts directly with buttons and a dropdown, tied to the message ID. This drops webhooks (two fewer secrets) and the filename-in-text matching. | adopted |
| 2026-10-18 | Drop Gmail; the daily summary moves to Discord. Telegram may replace Discord later, so keep the notifier behind a small interface. | adopted (Adam) |
| 2026-10-18 | Keep a NABirds subset for the tray species with no local labels yet (American Goldfinch, Dark-eyed Junco), as cold-start data. Archive the rest. | adopted |
| 2026-10-18 | Added White-throated Sparrow to the dropdown (a common winter ground feeder in Black-capped Chickadee range) alongside the Red-breasted Nuthatch Adam approved. | open: Adam to confirm |
