"""Sprite animation state machine."""

from __future__ import annotations

from typing import Dict, List

import pygame


class AnimationController:
    """Cycle through frames based on an animation state."""

    def __init__(self, frames: Dict[str, List[pygame.Surface]], fps: int = 10):
        self._frames = frames
        self._fps = fps
        self._current = "idle" if "idle" in frames else next(iter(frames))
        self._time = 0.0
        self._index = 0
        self._flip = False

    def set_state(self, state: str, flip: bool | None = None) -> None:
        """Change animation state and optionally flip horizontally."""
        if state != self._current:
            self._current = state
            self._index = 0
            self._time = 0.0
        if flip is not None:
            self._flip = flip

    def update(self, dt: float) -> None:
        """Advance the frame based on elapsed time."""
        frames = self._frames[self._current]
        self._time += dt
        if self._time >= 1 / self._fps:
            self._time -= 1 / self._fps
            self._index = (self._index + 1) % len(frames)

    @property
    def image(self) -> pygame.Surface:
        """Current frame image."""
        img = self._frames[self._current][self._index]
        return pygame.transform.flip(img, self._flip, False) if self._flip else img
