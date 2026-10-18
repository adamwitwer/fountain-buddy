# Fountain Buddy

A feeder camera that identifies its visitors and gets better at it from your answers.

1. The Reolink camera reports motion.
2. A burst of frames is checked by an object detector (YOLO) for birds.
3. The best crop is classified by a small model trained on top of a biology foundation
   model (BioCLIP 2), using every answer you have ever given.
4. Discord gets the photo with the top guesses as buttons.
5. You tap the right one (or Skip). That answer becomes training data; an unanswered
   post never does.

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

## Hardware

- Reolink RLC-810WA (4K, Wi-Fi) aimed at a safflower tray feeder.
- Mac mini (M4 Pro) that never sleeps.
- A Discord server with a bot that has Send Messages, Attach Files, Add Reactions and
  Read Message History in one channel.
