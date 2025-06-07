"""Collectible coin."""
from __future__ import annotations

import pygame

from ..core.animation import AnimationController


class Item(pygame.sprite.Sprite):
    """Simple collectible item."""

    def __init__(self, pos: pygame.Vector2, sprites: dict) -> None:
        super().__init__()
        self.anim = AnimationController(sprites, 'idle')
        self.image = self.anim.frame
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, dt: float) -> None:
        self.anim.update(dt)
        self.image = self.anim.frame
