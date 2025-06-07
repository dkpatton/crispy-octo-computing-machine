"""Camera system to convert world coordinates into screen coordinates."""

from __future__ import annotations

import pygame


class Camera:
    """Follow a target entity while clamping to the level bounds."""

    def __init__(self, screen_size: tuple[int, int], level_bounds: pygame.Rect):
        self._screen_size = pygame.Vector2(screen_size)
        self._bounds = level_bounds
        self._pos = pygame.Vector2(0, 0)
        self._deadzone = pygame.Rect(
            screen_size[0] // 3, screen_size[1] // 3, screen_size[0] // 3, screen_size[1] // 3
        )

    def update(self, target: pygame.sprite.Sprite) -> None:
        """Move the camera toward the target while keeping within level bounds."""
        tx, ty = target.rect.centerx, target.rect.centery
        if tx - self._pos.x < self._deadzone.left:
            self._pos.x = tx - self._deadzone.left
        elif tx - self._pos.x > self._deadzone.right:
            self._pos.x = tx - self._deadzone.right

        if ty - self._pos.y < self._deadzone.top:
            self._pos.y = ty - self._deadzone.top
        elif ty - self._pos.y > self._deadzone.bottom:
            self._pos.y = ty - self._deadzone.bottom

        self._pos.x = max(0, min(self._pos.x, self._bounds.width - self._screen_size.x))
        self._pos.y = max(0, min(self._pos.y, self._bounds.height - self._screen_size.y))

    def world_to_screen(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates."""
        return int(pos[0] - self._pos.x), int(pos[1] - self._pos.y)
