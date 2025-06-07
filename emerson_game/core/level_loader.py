"""Load level data from JSON."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pygame

from .asset_loader import load_json
from . import settings


class Level:
    """Representation of a loaded level."""

    def __init__(self) -> None:
        self.platforms = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.size: Tuple[int, int] = (0, 0)
        self.player_start = pygame.Vector2(0, 0)


class TileSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


def load_level(path: str, tileset: pygame.Surface) -> Level:
    data = load_json(path)
    level = Level()
    level.size = data.get('size', [20, 15])
    tile_w, tile_h = settings.TILE_SIZE, settings.TILE_SIZE

    for y, row in enumerate(data.get('tiles', [])):
        for x, tile in enumerate(row):
            if tile == 1:
                img = tileset
                sprite = TileSprite(img, (x * tile_w, y * tile_h))
                level.platforms.add(sprite)

    px, py = data.get('player_start', [0, 0])
    level.player_start = pygame.Vector2(px, py)
    return level
