# Fountain Buddy: rebuild plan

Written 2026-10-18 at the start of the rebuild. This is the source of truth for scope and
order of work until the rebuild ships; after that, `AGENTS.md` takes over and this file
becomes history. Tick boxes as phases land, and record decisions here when they change.

## Goal (unchanged)

The camera sees motion → snap photos → find the bird → guess the species → post to
Discord → a human confirms or corrects → the model gets better from those answers.
An unanswered post is **not** a confirmation and never trains the model.

## Decisions (Adam, 2026-10-18)

- **One camera: Tray Feeder**, Reolink RLC-810WA (4K, Wi-Fi) at 192.168.50.249. It is
  the old Peanut Feeder camera, moved and renamed. The old CAMERA1 login works on it.
- **Runs on the Mini M4 Pro** (this machine, 48 GB, LAN 192.168.50.x). Adam is setting it
  to never sleep. The project lives on the external `Envoy` volume, so a launchd job
  needs permission to read it, and the drive must be mounted at boot.
- **Fresh public repo** (approved and done 2026-10-18). The old repo has every secret in
  its history (see Phase 0), so instead of rewriting history the new code starts with
  clean history. The old GitHub repo is now `fountain-buddy-legacy` (private, archived),
  and the new repo takes the `fountain-buddy` name. Locally, the old checkout is at
  `/Volumes/Envoy/apps/fountain-buddy-legacy`, and the new repo stays at this path, so
  Claude's project memory carries over.
- **No Gmail.** The daily summary moves to Discord.
- **Discord for now.** Telegram may replace it later, so keep the notifier behind a
  small interface (as `nudge` does), but don't build Telegram yet.
- **Archive old data** that no longer has value. Disk is not tight (3.2 TB free), so
  "archive" means moving it into the legacy folder, not deleting it.
- **Tray seed is safflower.** Expected species: Northern Cardinal, Tufted Titmouse,
  House Finch, American Goldfinch, Mourning Dove, Black-capped Chickadee (confirmed),
  Dark-eyed Junco, White-breasted Nuthatch. Red-breasted Nuthatch goes in the dropdown
  (Adam has never seen one, but no harm). Safflower tends to put
  off House Sparrows, starlings, grackles and squirrels, but expect some anyway.

## What we found (2026-10-18 review)

- **Leaked secrets.** `services/com.fountainbuddy.{service,discordbot}.plist` were
  committed in `18cca1d` (2025-08-03) with every secret in `EnvironmentVariables`. All
  current `.env` values are in public history: Discord bot token, both webhooks, Gmail app
  password, camera password. Webhook URLs also appear in four commits from 2025-07-01.
- **Labels are the asset.** `fountain_buddy.db` has 7,884 visits (2025-06-28 → 2025-12-26)
  and 3,636 human verifications: about 3,250 species IDs across 18 species, plus 379
  "Skip". Every verified image is still on disk.
- **The old classifier failed in the field.** EfficientNetV2B0 trained mostly on NABirds:
  0.68 test accuracy, but it agreed with the human in only 25 of 549 Aug 2025 posts. Its
  most common miss was "Downy Woodpecker" on frames the human skipped. Not worth saving.
- **Saved images are marked up.** The YOLO box and label are drawn into every saved JPEG
  (full 3840×2160 frames). Training crops must be cut from inside the drawn box.
- **Mislabeled location.** Dec 2025 rows tagged `fountain` came from the Peanut Feeder
  camera (the camera's own overlay says so).
- **Why it stopped:** polling `GetMdState`/`GetAiState` every second ended in an endless
  "please login first" loop. No services are running. The Dec 2025 refactor (`core/`,
  `services/`, `ml/`, `config/`) was never committed.
- **Camera abilities:** built-in AI detection for people, vehicles and dog/cat (no bird
  class). Ports 80, 443, 554 (RTSP) and 9000 (Baichuan push) are open.
- **NABirds still has some use.** It covers every tray species, including goldfinch and
  junco, which have zero local labels. Keep that subset as cold-start data.

## Architecture (target)

One Python process, asyncio, run by launchd on the Mini:

1. **Trigger:** camera push events through `reolink_aio` (Baichuan, port 9000) instead of
   polling. Motion is only a hint; the detector decides.
2. **Capture:** a short burst from the RTSP main stream (falling back to HTTP `Snap`).
   Save the raw frame unmarked. Only the Discord copy gets a box drawn on it.
3. **Detect:** YOLO26 (Ultralytics' current model) on MPS, COCO class `bird`. It throws
   out empty frames and picks the best crop across the burst.
4. **Classify:** a frozen foundation model to turn each crop into a feature vector, plus a
   small classifier on top trained on our labels, including a "not usable" class learned
   from the Skips. Retraining takes seconds, so it can happen after every few answers. A
   zero-shot fallback over the species list covers birds with no labels. Candidates:
   **BioCLIP 2** (expected winner) and DINOv3; Phase 3 picks one using measured results.
   Optional later: Claude vision as a second opinion when confidence is low.
5. **Discord:** the bot posts directly (no webhooks). Each post has the top 3 guesses as
   buttons, an "Other…" dropdown with the full species list, and Skip / Not a bird. Each
   answer is tied to its message ID, so no more matching filenames out of the text. A
   typed reply still works.
6. **Learning loop:** a new model replaces the old one only if it scores at least as well
   on held-out photos. A weekly Discord post shows how often the model and the human
   agreed.
7. **Liveness:** a healthchecks.io ping, a Discord alert when the camera drops, and a
   startup smoke test (the pattern `nudge` uses).

Stack: Python 3.12+, `uv` + `pyproject.toml`, PyTorch (MPS), `open_clip`/`timm`,
`ultralytics`, `reolink_aio`, `discord.py`, scikit-learn, SQLite, pytest, ruff.
No TensorFlow.

Data: runtime data (images, DB) lives in `data/`, gitignored, with a test that fails if
git ever tracks an image, database, `.env` or plist.

## Phases

### Phase 0: Lock down

- [x] Adam: reset the Discord bot token. Verified 2026-10-18: new token works, not in
      any leaked copy.
- [x] Adam: delete the old webhooks. Verified: all 4 URLs in history return 404.
- [x] Adam: revoke the Gmail app password (Gmail is being dropped).
- [x] Adam: change the camera password. Verified: `check` logs in with a password that
      is in no leaked copy. Phase 0 closed 2026-10-18.
- [x] Claude: rename the old GitHub repo to `fountain-buddy-legacy`, private, archived.
- [x] Claude: add an entry to `~/Documents/Projects/SECURITY-LOG.md`.
- [x] Convert `.env` to the new keys (Claude, by script, 2026-10-18).

### Phase 1: New repo

- [x] Move the old checkout to `fountain-buddy-legacy`, then `git init` a new repo here.
- [x] `fountain_buddy/` package, `pyproject.toml` (uv), pytest, ruff, `.env.example`.
- [x] `uv run fountain-buddy check`: settings booleans, camera login and snapshot.
- [x] `AGENTS.md` (conventions, current status, agent input log in the style of
      `reminders/AGENTS.md`), plus a `CLAUDE.md` that contains only `@AGENTS.md`.
- [x] Strict `.gitignore`, plus `scripts/hygiene.py` as a test and a pre-commit hook.
- [x] Move `bird_images/` and `fountain_buddy.db` into `data/images/` and `data/legacy.db`.
- [x] First commit; create the public `adamwitwer/fountain-buddy` and push (`8f876d7`).

### Phase 2: Rescue the data

- [x] New schema (`fountain_buddy/db.py`): visits, crops, labels, predictions, and a
      `current_labels` view. Human labels are kept apart from model output.
- [x] `fountain-buddy import-legacy` (idempotent): 7,884 visits, 3,653 human labels
      (including 17 skip replies that v1 stored as `archived_poor_quality`), and 4,104
      v1 predictions as a baseline. Names normalized. Dec 2025 rows re-tagged
      `legacy-peanut`.
- [x] Crops cut from just inside v1's drawn green box (it marks the bird the human
      labeled): 3,501 of 3,653 (96%). 150 have no recoverable box (box hidden or broken
      up by foliage), and 2 images are missing. YOLO re-detection can recover those later.
- [x] Time split (oldest 80% train, newest 20% test) lives in `bakeoff.time_split`.
- [x] NABirds subset: 3,825 bounding-box crops for all 22 species in `data/nabirds/`
      (322 MB), including American Goldfinch (240) and Dark-eyed Junco (362), which have
      no local labels. The full dataset, `training_data_enhanced_cnn/`, the old models
      and the old venv stay archived in the legacy folder.

### Phase 3: Model bake-off (on our data, not published benchmarks)

- [x] Detection: YOLO26 vs yolov8n, measured by how many labeled birds each finds. Best
      off-the-shelf is yolo26m@1280 at 54–71% recall, which is too low.
- [x] Fine-tune YOLO26 on our ~3,500 verified boxes (drawn lines inpainted out first).
      **Rejected 2026-10-18.** YOLO26s@1280, 50 epochs (5.3 h): 99.5% recall on v1's
      held-out frames, but it learned v1's old backgrounds. On the new tray scene it
      missed one of the first two wrens and fired on the white cable (AGENTS.md, "Model
      choices"). Redo once the tray has a few hundred labeled visits of its own.
- [x] Classification: BioCLIP 2 head (local + NABirds) blended with zero-shot. 81.5%
      top-1, 98.3% top-3, 91.5% on birds; v1 was 7.3%.
- [x] Pick, and record the numbers in AGENTS.md ("Model choices").

### Phase 4: Live pipeline

- [x] Camera events → burst → detect → classify → Discord post with buttons (`9c2776f`).
      A test post rendered correctly; the service went live 2026-10-18 15:09, run from
      a Claude session until Phase 6 (launchd). Interim detector: yolo26m@1280, conf 0.1.
- [x] ~~Swap in the fine-tuned detector~~: not swapped (see Phase 3). Stock
      yolo26m@1280, conf 0.1 stays. First real birds: two Carolina Wrens, 2026-10-18
      18:28 and 18:29, both found, both guessed right, both confirmed by Adam.
- [ ] Run alongside Adam for a few days before it counts.

### Phase 5: Learning loop

- [ ] Retrain the small classifier as answers come in, accept only on equal or better
      held-out results, and post the weekly agreement report. Progress:
  - [x] 2026-10-18: gated `classifier.retrain` (`train-head [--force]`), `trainings`
        table, old heads pruned to 10. One fit takes 0.2 s and a whole retrain about
        5 s, so it can run after every answer instead of nightly. **Gate:** the test
        set is the newest 20% of the labels the current head already had. The current
        head's labels and all labels are each fit without those rows and scored on
        them. Accept if top-1 and top-3 are no more than 0.5 points worse. This asks
        "do the new answers make it worse?" and can't block learning just because
        tray photos are harder than v1's. Tested on synthetic features: good answers
        accepted, 150 mislabels rejected, `--force` overrides.
  - [x] 2026-10-18: Service retrains 60 s after the last answer (on the model thread,
        so never during a detection), and once at startup. It posts in Discord only
        when a retrain is rejected or fails, and once more when it recovers. `status`
        shows the last retrain.
  - [x] 2026-10-18: Weekly report in Discord (Sundays after the daily summary) and
        `fountain-buddy report`. It covers first-guess agreement, whether the answer was
        a button, per species, mix-ups, and retrains. Every guess was made before its
        answer existed, so this is the honest live score.
  - [x] 2026-10-18 22:46: deployed. The startup retrain picked up Adam's two wren
        answers. Gate: top-1 81.4% vs 81.7% on 698 crops (2 crops apart, within
        tolerance; a strict >= would have refused 2 correct answers), top-3 98.7%
        vs 98.6%. Accepted, live as `head-20261018-224659`, about 3 s end to end.
  - [ ] See it retrain after a real tap in Discord (the startup path is verified;
        the tap hook is one callback).
- [ ] Retrain the detector on tray frames once there are a few hundred labeled visits:
      the bird boxes the live detector found (checked by Adam's label), plus empty tray
      frames from `data/rejects/` as negatives so the cable and seed stop scoring. Test
      on the newest tray visits, never on v1's scenes alone.

### Phase 6: Run for real

- [x] LaunchAgent `com.fountainbuddy.run` via `launchd/install.sh` (template has no
      secrets). Live since 2026-10-18 16:19. Crash recovery verified: back 31 s after
      `kill -9`.
- [x] macOS permissions granted for Homebrew python3.13: Removable Volumes and Local
      Network (see AGENTS.md "Deploying").
- [x] Camera-down alert in Discord after 15 min. Camera connect times out (60 s) instead
      of hanging.
- [x] Deploy notes in AGENTS.md.
- [x] ~~healthchecks.io~~ declined by Adam (overkill). Instead: `status` in Discord, the
      `fountain-buddy status` CLI, and README "Is it running?".

## Open questions

- None right now. (Settled 2026-10-18: White-throated Sparrow stays in the dropdown.)
