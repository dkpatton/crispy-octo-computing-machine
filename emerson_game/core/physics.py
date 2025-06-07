"""Simple axis-aligned physics engine."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pygame

from . import settings


@dataclass
class Body:
    rect: pygame.Rect
    vel_x: float = 0.0
    vel_y: float = 0.0
    on_ground: bool = False


class PhysicsEngine:
    """Apply gravity and resolve basic collisions."""

    GRAVITY = 800
    JUMP_SPEED = -250
    TERMINAL_VELOCITY = 400

    def __init__(self, platforms: pygame.sprite.Group) -> None:
        self.platforms = platforms

    def apply_gravity(self, body: Body, dt: float) -> None:
        body.vel_y = min(body.vel_y + self.GRAVITY * dt, self.TERMINAL_VELOCITY)

    def move(self, body: Body, dt: float) -> None:
        body.rect.x += int(body.vel_x * dt)
        self._collide_axis(body, 'x')
        body.rect.y += int(body.vel_y * dt)
        self._collide_axis(body, 'y')

    def _collide_axis(self, body: Body, axis: str) -> None:
        hits = [s for s in self.platforms if s.rect.colliderect(body.rect)]
        for sprite in hits:
            if axis == 'x':
                if body.vel_x > 0:
                    body.rect.right = sprite.rect.left
                elif body.vel_x < 0:
                    body.rect.left = sprite.rect.right
                body.vel_x = 0
            else:
                if body.vel_y > 0:
                    body.rect.bottom = sprite.rect.top
                    body.on_ground = True
                elif body.vel_y < 0:
                    body.rect.top = sprite.rect.bottom
                body.vel_y = 0
