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
- Phase 2: done. v1's labels are in `data/fountain_buddy.db` (3,501 with crops).
- Phase 3: done. BioCLIP 2 head + zero-shot (see "Model choices"). The fine-tuned
  YOLO26s detector was rejected: it learned v1's backgrounds and fails on the tray.
  Stock yolo26m@1280 stays.
- **The tray feeder was installed 2026-10-18.** Birds take days to discover a new
  feeder, so a quiet first few days is expected, not a fault. Camera motion detection is
  at maximum sensitivity (sensDef 1, i.e. 50/50 in the app) over the whole frame.
- Phase 4: done. Adam's first tap (on a TEST post) and a hand-wave motion test both
  worked end to end on 2026-10-18.
- Phase 6: done. Live under launchd since 2026-10-18 16:19 (see "Deploying").
  healthchecks.io was declined; liveness is the Discord `status` reply plus the
  camera-down alert (README, "Is it running?").
- First real birds: two Carolina Wrens at 18:28 and 18:29 on 2026-10-18, found by the
  detector and guessed right by the classifier.
- Phase 5: classifier learning loop live since 2026-10-18 22:46. It retrains a minute
  after answers stop, gated (see Conventions), and posts a weekly report on Sundays. A retrain
  after real taps was verified 2026-10-19. Left: the detector retrain on tray frames
  once there are a few hundred tray visits (PLAN.md).
- Night visitors: a mouse works the tray all night. It made 94 posts overnight
  2026-10-19/20, too many to answer one by one. **Infrared rule** (2026-10-20): the camera's
  night frames are pure greyscale (mean HSV saturation 0; daylight 38–70), so an infrared
  burst posts only if the classifier's first guess is a species or Squirrel. Otherwise
  it goes to `data/rejects/<day>/*-night.jpg`, and `status` counts it. Night isn't "no
  posts": the camera stays in infrared past sunrise, and a Carolina Wren came at 07:35
  in infrared. Replayed with the then-current head: all 109 infrared non-birds dropped,
  the wren kept.
- First Northern Cardinals: 2026-10-20 11:56, then 4 posts at 16:40. Soft focus at that
  distance (see the camera-placement log entry).
- **Known not-a-bird spots** (2026-10-19). In low light the tray's bracket kept scoring as
  a bird. That was 14 posts of the same box, (1728,1580)–(2138,1813), mostly at dusk. A
  detection whose box matches (IoU >= 0.5; 0.7 until 2026-10-20) a box Adam answered
  "Not a bird" in the last 30 days is now dropped unless the classifier's first guess is a species or Squirrel. A
  bird elsewhere in the burst beats any detection on a spot. Dropped frames go to
  `data/rejects/<day>/*-spot.jpg`, and `status` counts them. Replayed on all 34 live
  visits before deploying: every bracket post dropped, all 5 wrens kept; first live drop
  at 19:06 the same day.
  Loosened to IoU 0.5 on 2026-10-20 for an ivy sprig on the deck (bottom left) that
  sways: its repeats overlap each other at IoU 0.2–0.9. Overlap with the smaller box
  would be looser still, but in replay it dropped a wren standing inside the bracket's
  box, so it's plain IoU.

## Commands

```bash
uv sync                          # .venv, Python 3.13
uv run fountain-buddy check      # settings + camera login
uv run fountain-buddy run        # the service (camera, models, Discord), one process
uv run fountain-buddy status     # is it up? launchd state, last start, warnings, camera
uv run fountain-buddy train-head [--force]  # gated retrain (the service does this itself)
uv run fountain-buddy report     # the weekly agreement report, last 7 days
uv run fountain-buddy post-test IMAGE   # post a TEST sighting (source='test', never trained)
uv run fountain-buddy import-legacy     # v1 import (idempotent; already done)
uv run fountain-buddy bakeoff [--detectors]   # Phase 3 comparisons -> data/reports/
uv run pytest                    # run before every commit
uv run ruff check . && uv run ruff format --check .
git config core.hooksPath .githooks   # once per clone: the secrets/data guard
```

## Deploying (Mini M4 Pro, LaunchAgent)

```bash
launchd/install.sh               # install, or reinstall after a code change (restarts it)
launchctl kickstart -k gui/$(id -u)/com.fountainbuddy.run   # restart only
launchctl print gui/$(id -u)/com.fountainbuddy.run | grep -E 'state|pid|runs|last exit'
launchd/install.sh uninstall
```

- App log: `data/logs/fountain-buddy.log` (rotating). launchd's own log
  (`~/Library/Logs/fountain-buddy.launchd.log`) gets warnings and up only.
- **A deploy isn't done until a fresh `service: running` line appears** after the restart.
  Check the log, not just `launchctl print`: under a pending permission prompt the process
  shows `state = running` while doing nothing.
- **Two macOS permissions are needed, and both attach to Homebrew's python binary**
  (`/opt/homebrew/Cellar/python@3.13/3.13.15/...`, which `.venv` points to):
  1. *Removable Volumes*, because the repo is on the external `Envoy` drive. Without it
     the process blocks silently at startup (TCC `AUTHREQ_PROMPTING` in
     `log show --predicate 'subsystem == "com.apple.TCC"'`) and writes nothing.
  2. *Local Network*, to reach the camera. Without it the camera connect fails with
     `[Errno 65] No route to host`.
  A `brew upgrade` that moves python to a new Cellar path will prompt again and pause
  the service until someone clicks Allow on the Mini. After any Python upgrade, re-run
  `uv sync`, `launchd/install.sh`, and check for the `service: running` line.
- **Homebrew `python@3.13` is pinned** (`brew pin`, 2026-10-18) so an upgrade can't
  silently move the binary the permissions are tied to. To upgrade on purpose:
  `brew unpin python@3.13 && brew upgrade python@3.13`, then `uv sync`,
  `launchd/install.sh`, and click Allow on the Mini twice.
- `install.sh` waits for `bootout` to finish before `bootstrap`. Without the wait, a
  quick reinstall fails with "Bootstrap failed: 5: Input/output error" and leaves the
  service **unloaded** (it happened once, 2026-10-18 16:27).
- It is a LaunchAgent (runs in Adam's login session). With FileVault on, nothing could
  start before login anyway, so after a power cut it starts once Adam logs in.
- Only one copy may run. Two would double-post and fight over button taps, so stop any
  `fountain-buddy run` in a terminal before installing.

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
- **Build `Service` inside the event loop.** reolink_aio's `Host` creates an aiohttp
  connector in its constructor, which needs a running loop. Constructing it outside one
  crashed both `post-test` and `run` on the first try.
- **Model pointers, not hard-coded paths.** `data/models/head.json` names the current
  classifier head (hot-reloaded). `data/models/detector.json` names the detector weights,
  imgsz and conf (read at startup; default yolo26m@1280, conf 0.1). Ultralytics weights
  live in `data/models/`, never the repo root.
- **Write plain Python ints to SQLite.** numpy integers are stored as 8-byte BLOBs and
  silently break comparisons (it happened to the crop coordinates on 2026-10-18).
- **Never trust a single motion source.** Push events can drop, so `camera.watch` also
  polls motion state every 3 s. Only the initial state push has been seen so far; check
  the first real motion in the log.
- **Python 3.13, uv-managed.** No TensorFlow. PyTorch on MPS.
- **Measure models on our own photos, split by time** (older to train, newer to test). A
  retrained model replaces the current one only if it scores at least as well.
  - For the classifier, `classifier.retrain` enforces that. Both heads are fit without
    the gate set (the newest 20% of labels the current head had) and scored on it.
    "As well" means top-1 and top-3 within 0.5 points: two new answers moved top-1 by
    2 of 698 crops on the first live run. Every attempt goes in the `trainings` table.
  - The weekly report's agreement is the honest live score: every guess was made
    before its answer existed. Judge the model by that, not by held-out numbers.
- Run `pytest` before every commit. After a search-and-replace edit, grep to confirm it
  landed.

## Model choices (Phase 3, 2026-10-18)

Measured on our own labeled crops, time split (train through 2025-08-12, test the newest
701 crops, 2025-08-12 to 2025-10-07). Full tables are in `data/reports/`; rerun with
`fountain-buddy bakeoff` and `fountain-buddy bakeoff --detectors`.

**Classifier: BioCLIP 2, frozen, plus a logistic-regression head** trained on our
labels plus NABirds crops (weight 0.5, C=30), blended with BioCLIP 2 zero-shot
(geometric mix, alpha 0.3) over the species part of the distribution.

| variant | top1 | top3 | birds top1 | macro recall | ECE | skip recall |
|---|---|---|---|---|---|---|
| v1 EfficientNet (baseline) | 7.3% | | | | | |
| BioCLIP 2 head, local + NABirds | 81.7% | 98.4% | 91.5% | 85.7% | 0.036 | 53.6% |
| BioCLIP 2 head + zero-shot 0.3 (**chosen**) | 81.5% | 98.3% | 91.5% | 87.6% | 0.027 | 52.5% |
| BioCLIP 2 zero-shot only, birds | 92.7% | 96.5% | 92.7% | 91.9% | 0.033 | n/a |
| DINOv3-L head, local + NABirds | 83.7% | 98.1% | 91.3% | 83.1% | 0.018 | 61.9% |
| BioCLIP 2 + DINOv3-L concat head | 82.9% | 98.9% | 90.8% | 82.5% | 0.027 | 60.2% |

- BioCLIP 2 identifies species best, and its zero-shot is strong enough (92.7% on our
  birds with no training) to cover species with no local labels (goldfinch, junco).
- **Skip is the weak spot** for every model (52–62% recall). Some of that is label
  noise: Skip was a judgment call. Every photo goes to Discord anyway, so a missed Skip
  costs one tap.
- DINOv3 helps Skip a little, but a second ViT-L on every frame wasn't worth +1 point.
- House Sparrow recall (80%) loses mostly to Skip. Song Sparrow (5 test crops) was 0%.

**Detector: off-the-shelf COCO YOLO is the bottleneck.** Recall of the bird the human
labeled (IoU >= 0.3 with v1's drawn box) on 400 labeled 4K photos:

| detector | conf>=0.25 | conf>=0.1 | conf>=0.05 | ms/frame (M4 Pro, MPS) |
|---|---|---|---|---|
| yolov8n@640 (v1) | 42.2% | | | 7 |
| yolo26s@1280 | 45.2% | 57.8% | 63.8% | 21 |
| yolo26m@1280 | 54.2% | 64.5% | 70.8% | 43 |
| yolo26l@1280 | 43.5% | 51.8% | 58.5% | |

COCO birds score 0.15–0.3 on these frames, and some are called "cat". v1 got by
because its burst kept the best of 5 frames at a low threshold.

**Those frames have v1's green boxes drawn on them, and the boxes hurt stock YOLO.** With
the boxes inpainted out (623 held-out frames, `data/reports/detector-finetune-*.md`):

| detector | recall @0.5 | @0.25 | @0.1 | ms |
|---|---|---|---|---|
| yolo26s@1280 stock | 67.1% | 82.2% | 90.0% | 21 |
| yolo26m@1280 stock (**chosen**) | 85.2% | 92.9% | 94.9% | 43 |
| yolo26s@1280 fine-tuned on v1 boxes | 99.5% | 99.7% | 99.8% | 21 |

**The fine-tune was rejected anyway.** Every v1 frame came from the old fountain and
peanut-feeder views, so the test set shared their backgrounds. On the tray scene (2
wren visits, 69 empty frames) it missed one wren, scored the other 0.18, and fired on
the white cable bundle at up to 0.27. Stock yolo26m found both wrens (0.19, 0.45) and
nothing on the empty frames. Lesson: **a detector test set must include the current
scene.** Retrain on tray frames once they exist (PLAN.md, Phase 5). Our fine-tuned
weights use class 0 for "bird", stock COCO uses 14; `Detector` reads it from the
weights' names.

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
| 2026-10-20 | Handle the night mouse by camera mode, not by clock or by more answers. Infrared frames are exactly greyscale, so the signal is free and needs no sunrise table. Infrared posts need a species as first guess. Dropping every infrared burst would have lost a 07:35 wren. Answering each mouse "Not a bird" doesn't stop posts, because a moving mouse never matches a known spot. Rejected frames are kept 7 days in `rejects/` if a missed night bird ever needs checking. | done |
| 2026-10-19 | Adam is weighing a new camera placement (or camera): the tray is too close for the fixed-focus lens to focus. Until it's settled, hold the detector retrain on tray frames. After a move: clear the known not-a-bird spots (their boxes belong to the old view), keep the classifier's tray labels (birds look the same), and compare crop sharpness before and after. A replacement should be a Reolink if possible, since `camera.py` relies on reolink_aio for motion events. 2026-10-21: Adam plans to move it higher, to the side and further back (same camera). The infrared rule doesn't depend on the view, so the mouse stays handled through the move. | open |
| 2026-10-19 | Drop detections at known not-a-bird spots rather than raising the detector threshold or trusting the classifier alone. The bracket scored up to 0.44, above two real wrens (0.23, 0.27), so no threshold separates them. And "classifier says Not a bird" alone would hide a dim bird it gets wrong. Requiring both the spot (from Adam's answers) and a non-species guess keeps a cardinal on the bracket visible. | done |
| 2026-10-18 | Retrain after every answer (debounced 60 s), not nightly. A whole retrain takes ~3 s, so there is no reason to make new tray species wait a day. The gate compares like with like (same held-out rows, neither model trained on them) instead of each head's own held-out score, which would drift as tray photos (a harder, newer scene) take over the test split and then block learning for no real reason. | done |
| 2026-10-18 | Tray answers carry the same weight as v1's 3,489 legacy answers, so the new scene is ~0.1% of the training set at first. If the weekly report shows tray agreement lagging, up-weight live labels (e.g. ×3) and let the gate judge it. | open |
| 2026-10-18 | Night IR frames trip motion at max sensitivity (about 55 empty bursts after dusk on day one). Harmless: no posts, ~0.2 s of compute each, rejects pruned after 7 days. Could skip bursts while the camera is in night mode if it ever matters. | done (2026-10-20, see the 2026-10-20 entry) |
| 2026-10-18 | Liveness: suggested healthchecks.io (it catches a dead Mini, which nothing on the Mini can report). Adam: overkill. Instead the bot answers `status` in Discord, and `fountain-buddy status` covers the terminal. Known gap: if the whole Mini or the service is down, nothing posts, so a silent channel for days during busy bird season is the hint to type `status`. | declined (healthchecks); done (status) |
| 2026-10-18 | Start a fresh public repo instead of rewriting v1's history. A force-push leaves the old commits reachable by SHA on GitHub, and rotating the secrets is the real fix anyway. v1 was renamed `fountain-buddy-legacy`, made private and archived. This repo took the name. | done |
| 2026-10-18 | Replace the TF CNN with frozen foundation-model features plus a small classifier trained on Adam's labels. The CNN was trained mostly on NABirds' professional photos and failed on the feeder camera. A small head retrains in seconds, so the model can learn after every few answers. BioCLIP 2 vs DINOv3 is decided by a bake-off on our data (Phase 3). | adopted |
| 2026-10-18 | Discord bot posts directly with buttons and a dropdown, tied to the message ID. This drops webhooks (two fewer secrets) and the filename-in-text matching. | adopted |
| 2026-10-18 | Drop Gmail; the daily summary moves to Discord. Telegram may replace Discord later, so keep the notifier behind a small interface. | adopted (Adam) |
| 2026-10-18 | Keep a NABirds subset for the tray species with no local labels yet (American Goldfinch, Dark-eyed Junco), as cold-start data. Archive the rest. | adopted |
| 2026-10-18 | Added White-throated Sparrow to the dropdown (a common winter ground feeder in Black-capped Chickadee range) alongside the Red-breasted Nuthatch Adam approved. | adopted (Adam, 2026-10-18) |
