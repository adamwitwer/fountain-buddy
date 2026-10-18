"""The Reolink camera: motion triggers and snapshot bursts, through reolink_aio.

Motion arrives as Baichuan push events (port 9000). A slow poll of the motion state backs
the push up, so one dropped push can't lose a bird. reolink_aio re-logs in on its own;
v1 polled by hand every second and died in a "please login first" loop.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import time
from collections.abc import Awaitable, Callable

import cv2
import numpy as np
from reolink_aio.api import Host

log = logging.getLogger(__name__)

POLL_SECONDS = 3
RESUBSCRIBE_SECONDS = 60
BURST = 4
BURST_GAP_SECONDS = 0.6
# A connect can hang rather than fail (seen 2026-10-18 when macOS blocked LAN access).
CONNECT_TIMEOUT_SECONDS = 60


class Camera:
    def __init__(self, host: str, username: str, password: str):
        self.host = Host(host, username, password, timeout=15)
        self.address = host
        self.last_ok = 0.0
        self._motion = asyncio.Event()

    async def connect(self) -> None:
        await asyncio.wait_for(self._connect(), CONNECT_TIMEOUT_SECONDS)

    async def _connect(self) -> None:
        await self.host.get_host_data()
        self.host.baichuan.register_callback("fountain-buddy", self._on_push)
        await self.host.baichuan.subscribe_events()
        self.last_ok = time.time()
        log.info(
            "camera: %r %s connected, push events on",
            self.host.camera_name(0), self.host.camera_model(0),
        )  # fmt: skip

    async def close(self) -> None:
        try:
            await self.host.baichuan.unsubscribe_events()
        finally:
            await self.host.logout()

    def _on_push(self) -> None:
        if self.host.motion_detected(0):
            self._motion.set()

    async def burst(self) -> list[np.ndarray]:
        """A few full-resolution frames, decoded to BGR."""
        frames = []
        for i in range(BURST):
            jpg = await self.host.get_snapshot(0, stream="main")
            if jpg:
                frame = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    frames.append(frame)
            if i < BURST - 1:
                await asyncio.sleep(BURST_GAP_SECONDS)
        if frames:
            self.last_ok = time.time()
        return frames

    async def watch(self, on_motion: Callable[[], Awaitable[None]]) -> None:
        """Call on_motion for each motion period, forever. Reconnects with backoff."""
        backoff = 5
        last_resub = time.time()
        while True:
            try:
                try:
                    await asyncio.wait_for(self._motion.wait(), POLL_SECONDS)
                except TimeoutError:
                    if not await self.host.get_motion_state(0):
                        if time.time() - last_resub > RESUBSCRIBE_SECONDS:
                            await self.host.baichuan.check_subscribe_events()
                            last_resub = time.time()
                        self.last_ok = time.time()
                        continue
                self._motion.clear()
                self.last_ok = time.time()
                await on_motion()
                backoff = 5
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # network, auth, camera reboot: keep going
                log.warning("camera: %s: %s; reconnecting in %ss", type(exc).__name__, exc, backoff)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 300)
                with contextlib.suppress(Exception):
                    await self.host.logout()
                try:
                    await self.connect()
                except Exception as exc2:
                    log.warning("camera: reconnect failed: %s", exc2)
