"""Simple walking enemy."""
from __future__ import annotations

import pygame

from ..core.animation import AnimationController
from ..core.physics import Body


class Enemy(pygame.sprite.Sprite):
    """Example Goomba-like enemy."""

    def __init__(self, pos: pygame.Vector2, sprites: dict) -> None:
        super().__init__()
        self.anim = AnimationController(sprites, 'walk')
        self.image = self.anim.frame
        self.rect = self.image.get_rect(topleft=pos)
        self.body = Body(self.rect, vel_x=-40)

    def update(self, dt: float) -> None:
        self.anim.update(dt)
        self.image = self.anim.frame
