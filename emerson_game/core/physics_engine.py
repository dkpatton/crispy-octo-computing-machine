"""Simple AABB physics with gravity and jumping."""

from __future__ import annotations

from typing import List

import pygame

from .constants import GRAVITY


class PhysicsEntity(pygame.sprite.Sprite):
    """Sprite subclass with velocity."""

    def __init__(self) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False

    def draw(self, surface: pygame.Surface, camera) -> None:
        pos = camera.world_to_screen(self.rect.topleft)
        surface.blit(self.image, pos)


class PhysicsEngine:
    """Update registered entities with physics."""

    def __init__(self) -> None:
        self.entities: List[PhysicsEntity] = []
        self.colliders: List[pygame.Rect] = []
        self.terminal_velocity = 500
        self.jump_strength = 300

    def add(self, entity: PhysicsEntity) -> None:
        self.entities.append(entity)

    def add_collider(self, rect: pygame.Rect) -> None:
        self.colliders.append(rect)

    def jump(self, entity: PhysicsEntity) -> None:
        if entity.on_ground:
            entity.vy = -self.jump_strength
            entity.on_ground = False

    def update(self, dt: float) -> None:
        for ent in self.entities:
            ent.vy = min(ent.vy + GRAVITY * dt, self.terminal_velocity)
            ent.rect.x += int(ent.vx * dt)
            self._collide(ent, "x")
            ent.rect.y += int(ent.vy * dt)
            self._collide(ent, "y")

    def _collide(self, ent: PhysicsEntity, axis: str) -> None:
        for col in self.colliders:
            if ent.rect.colliderect(col):
                if axis == "x":
                    if ent.vx > 0:
                        ent.rect.right = col.left
                    elif ent.vx < 0:
                        ent.rect.left = col.right
                    ent.vx = 0
                else:
                    if ent.vy > 0:
                        ent.rect.bottom = col.top
                        ent.on_ground = True
                    elif ent.vy < 0:
                        ent.rect.top = col.bottom
                    ent.vy = 0
