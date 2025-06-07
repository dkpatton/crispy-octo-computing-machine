"""Player entity."""
from __future__ import annotations

import pygame

from ..core.animation import AnimationController
from ..core.input_manager import InputState
from ..core.physics import Body


class Player(pygame.sprite.Sprite):
    """Hero controlled by the player."""

    def __init__(self, pos: pygame.Vector2, sprites: dict) -> None:
        super().__init__()
        self.anim = AnimationController(sprites, 'idle')
        self.image = self.anim.frame
        self.rect = self.image.get_rect(topleft=pos)
        self.body = Body(self.rect)

    def update(self, dt: float, input_state: InputState) -> None:
        if input_state.jump and self.body.on_ground:
            self.body.vel_y = -250
            self.body.on_ground = False
        self.body.vel_x = input_state.move_x * 100
        self.anim.update(dt)
        self.image = self.anim.frame
