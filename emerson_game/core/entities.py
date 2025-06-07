"""Game entity classes."""

from __future__ import annotations

import pygame

from .animation_controller import AnimationController
from .physics_engine import PhysicsEntity, PhysicsEngine
from .sprite_loader import SpriteLoader


class Player(PhysicsEntity):
    """Main controllable character."""

    def __init__(self, x: int, y: int, physics: PhysicsEngine):
        super().__init__()
        self._physics = physics
        self.anim = AnimationController(
            SpriteLoader.load_sheet("emerson_game/data/characters/hero.json")
        )
        self.image = self.anim.image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt: float, input_mgr) -> None:
        """Handle movement and animation state."""
        if input_mgr.left:
            self.vx = -120
            self.anim.set_state("walk", True)
        elif input_mgr.right:
            self.vx = 120
            self.anim.set_state("walk", False)
        else:
            self.vx = 0
            self.anim.set_state("idle")

        if input_mgr.jump:
            self._physics.jump(self)

        self.anim.update(dt)
        self.image = self.anim.image


class Zombie(PhysicsEntity):
    """Patrolling enemy."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.anim = AnimationController(
            SpriteLoader.load_sheet("emerson_game/data/characters/zombie.json")
        )
        self.image = self.anim.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = -60

    def update(self, dt: float, input_mgr) -> None:
        if self.rect.left <= 32 or self.rect.right >= 288:
            self.vx *= -1
        self.anim.set_state("walk", self.vx < 0)
        self.anim.update(dt)
        self.image = self.anim.image


class Coin(PhysicsEntity):
    """Collectible coin."""

    def __init__(self, x: int, y: int):
        super().__init__()
        frames = SpriteLoader.load_sheet("emerson_game/data/items/coin.json")
        self.anim = AnimationController(frames, fps=6)
        self.image = self.anim.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = self.vy = 0

    def update(self, dt: float, input_mgr) -> None:
        self.anim.update(dt)
        self.image = self.anim.image
