"""Load individual sprites and sprite sheets."""

from __future__ import annotations

import base64
import json
import os
import json
from typing import Dict, List

import pygame


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
            image_bytes = base64.b64decode(meta["data"])
            with open(path, "wb") as out:
                out.write(image_bytes)
            surface = pygame.image.load(path).convert_alpha()
            os.remove(path)
            return surface

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
