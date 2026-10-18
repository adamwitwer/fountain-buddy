"""SQLite store. Human labels and model predictions live in separate tables, and a
prediction is never promoted to a label.

Paths stored in the database are relative to the data dir, so the data can move.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS visits (
    id           INTEGER PRIMARY KEY,
    taken_at     TEXT NOT NULL,              -- local time, ISO 8601
    camera       TEXT NOT NULL,              -- 'tray'; legacy: 'legacy-fountain', 'legacy-peanut'
    image_path   TEXT,                       -- full frame, relative to the data dir
    frame_marked INTEGER NOT NULL DEFAULT 0, -- 1 if boxes/labels are drawn into the frame (v1)
    source       TEXT NOT NULL,              -- 'live' | 'legacy'
    legacy_id    INTEGER UNIQUE              -- bird_visits.id in v1's database
);

CREATE TABLE IF NOT EXISTS crops (
    id         INTEGER PRIMARY KEY,
    visit_id   INTEGER NOT NULL REFERENCES visits(id),
    method     TEXT NOT NULL,                -- 'drawn-box' (recovered from v1) or a detector name
    x1 INTEGER NOT NULL, y1 INTEGER NOT NULL, x2 INTEGER NOT NULL, y2 INTEGER NOT NULL,
    det_conf   REAL,                         -- detector confidence; NULL for drawn-box
    path       TEXT NOT NULL,                -- crop image, relative to the data dir
    UNIQUE (visit_id, method)
);

CREATE TABLE IF NOT EXISTS labels (
    id         INTEGER PRIMARY KEY,
    visit_id   INTEGER NOT NULL REFERENCES visits(id),
    label      TEXT NOT NULL,                -- canonical name from species.LABELS
    source     TEXT NOT NULL,                -- 'discord' | 'legacy'
    labeled_at TEXT NOT NULL,
    labeled_by TEXT
);
CREATE INDEX IF NOT EXISTS labels_visit ON labels(visit_id);

CREATE TABLE IF NOT EXISTS predictions (
    id           INTEGER PRIMARY KEY,
    visit_id     INTEGER NOT NULL REFERENCES visits(id),
    model        TEXT NOT NULL,
    label        TEXT NOT NULL,
    confidence   REAL,
    top_k        TEXT,                       -- JSON [[label, p], ...]
    predicted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS predictions_visit ON predictions(visit_id);

-- The current label for a visit is its most recent one.
CREATE VIEW IF NOT EXISTS current_labels AS
    SELECT l.* FROM labels l
    WHERE l.id = (SELECT MAX(id) FROM labels WHERE visit_id = l.visit_id);
"""


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init(path: Path) -> None:
    with closing(connect(path)) as conn:
        conn.executescript(SCHEMA)
