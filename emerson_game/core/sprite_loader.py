"""Load individual sprites and sprite sheets."""

from __future__ import annotations

import base64
import json
import os
from typing import Dict, List, Tuple

import pygame


def _parse_color(hex_color: str) -> Tuple[int, int, int, int]:
    """Convert #RRGGBB[AA] strings to RGBA tuples."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 8:
        r, g, b, a = (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
            int(hex_color[6:8], 16),
        )
    elif len(hex_color) == 6:
        r, g, b = (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
        a = 255
    else:
        raise ValueError(f"Invalid color: {hex_color}")
    return (r, g, b, a)

class SpriteLoader:
    """Utility class for loading images and sprite sheets."""

    @staticmethod
    def load_image(path: str) -> pygame.Surface:

        """Load a single image.

        If the PNG file does not exist on disk, a sidecar JSON file with the same
        path plus ``.json`` is checked. That JSON is expected to contain a base64
        encoded ``"data"`` field with the PNG bytes. The PNG is written
        temporarily to disk for loading and then removed.
        """

        if os.path.exists(path):
            return pygame.image.load(path).convert_alpha()

        json_path = f"{path}.json"
        if os.path.exists(json_path):
            with open(json_path) as fh:
                meta = json.load(fh)

            if "data" in meta:
                image_bytes = base64.b64decode(meta["data"])
                with open(path, "wb") as out:
                    out.write(image_bytes)
                surface = pygame.image.load(path).convert_alpha()
                os.remove(path)
                return surface

            if "palette" in meta and "grid" in meta:
                palette = [_parse_color(c) for c in meta["palette"]]
                grid = meta["grid"]
                height = len(grid)
                width = len(grid[0]) if height else 0
                surface = pygame.Surface((width, height), pygame.SRCALPHA)
                for y, row in enumerate(grid):
                    for x, ch in enumerate(row):
                        idx = int(ch)
                        color = palette[idx]
                        surface.set_at((x, y), color)
                return surface.convert_alpha()

        raise FileNotFoundError(path)

        """Load a single image."""
        return pygame.image.load(path).convert_alpha()

    @staticmethod
    def load_sheet(json_path: str) -> Dict[str, List[pygame.Surface]]:
        """Load a sprite sheet and slice frames per JSON metadata."""
        with open(json_path) as fh:
            meta = json.load(fh)
        sheet = SpriteLoader.load_image(meta["sprite_sheet"])
        frames: Dict[str, List[pygame.Surface]] = {}
        for state, rects in meta.get("frames", {}).items():
            frames[state] = [sheet.subsurface(pygame.Rect(r)) for r in rects]
        if frame := meta.get("frame"):
            frames["default"] = [sheet.subsurface(pygame.Rect(frame))]
        return frames
