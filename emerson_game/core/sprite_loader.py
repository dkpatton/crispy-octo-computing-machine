"""Load individual sprites and sprite sheets."""

from __future__ import annotations

import json
from typing import Dict, List

import pygame


class SpriteLoader:
    """Utility class for loading images and sprite sheets."""

    @staticmethod
    def load_image(path: str) -> pygame.Surface:
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
