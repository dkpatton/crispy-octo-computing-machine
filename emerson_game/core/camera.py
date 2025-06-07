"""Camera to convert world coordinates to screen coordinates."""
from __future__ import annotations

from dataclasses import dataclass

import pygame

from . import settings


@dataclass
class Camera:
    size: pygame.Vector2
    level_size: pygame.Vector2
    pos: pygame.Vector2

    def world_to_screen(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-self.pos.x, -self.pos.y)

    def update(self, target: pygame.Rect) -> None:
        self.pos.x = max(0, min(target.centerx - settings.SCREEN_WIDTH // 2, self.level_size.x - settings.SCREEN_WIDTH))
        self.pos.y = max(0, min(target.centery - settings.SCREEN_HEIGHT // 2, self.level_size.y - settings.SCREEN_HEIGHT))
