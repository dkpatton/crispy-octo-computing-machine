"""Load level JSON and spawn objects."""

from __future__ import annotations

import json
from typing import List

import pygame

from .camera import Camera
from .entities import Coin, Player, Zombie
from .physics_engine import PhysicsEngine, PhysicsEntity

TileMap = List[List[int]]


class Level:
    """Level container holding entities and metadata."""

    def __init__(
        self,
        width: int,
        height: int,
        tile_size: int,
        tiles: TileMap,
        entities: List[PhysicsEntity],
        player: Player,
    ):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = tiles
        self.entities = entities
        self.player = player
        self.bounds = pygame.Rect(0, 0, width * tile_size, height * tile_size)

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """Draw all level entities."""
        for ent in self.entities:
            ent.draw(surface, camera)


class LevelLoader:
    """Factory for loading levels."""

    @staticmethod
    def load(path: str) -> Level:
        with open(path) as fh:
            data = json.load(fh)

        width = data["width"]
        height = data["height"]
        tile_size = data["tile_size"]
        tiles: TileMap = data["tiles"]
        objects = data["objects"]

        physics = PhysicsEngine()
        entities: List[PhysicsEntity] = []

        player = Player(0, 0, physics)
        entities.append(player)

        for obj in objects:
            obj_type = obj["type"]
            x = obj["x"]
            y = obj["y"]
            if obj_type == "hero":
                player.rect.topleft = (x, y)
            elif obj_type == "zombie":
                entities.append(Zombie(x, y))
            elif obj_type == "coin":
                entities.append(Coin(x, y))

        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile == 1:
                    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    physics.add_collider(rect)

        level = Level(width, height, tile_size, tiles, entities, player)
        return level
