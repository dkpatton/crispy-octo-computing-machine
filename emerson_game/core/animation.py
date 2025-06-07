"""Simple animation controller for sprite states."""
from __future__ import annotations

from typing import Dict, List

import pygame


class AnimationController:
    """Manage animation frames for an entity.

    Example
    -------
    >>> animations = {
    ...     'idle': [Surface1, Surface2],
    ...     'run': [Surface3, Surface4],
    ... }
    >>> anim = AnimationController(animations, 'idle', 0.2)
    >>> anim.update(0.16)
    >>> current_image = anim.frame
    """

    def __init__(self, animations: Dict[str, List[pygame.Surface]], state: str, frame_time: float = 0.1) -> None:
        self.animations = animations
        self.state = state
        self.frame_time = frame_time
        self.timer = 0.0
        self.index = 0

    def update(self, dt: float) -> None:
        frames = self.animations[self.state]
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer -= self.frame_time
            self.index = (self.index + 1) % len(frames)

    @property
    def frame(self) -> pygame.Surface:
        return self.animations[self.state][self.index]

    def set_state(self, state: str) -> None:
        if state != self.state:
            self.state = state
            self.index = 0
            self.timer = 0.0
