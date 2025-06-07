"""Helpers for decoding base64-encoded assets and loading JSON data."""
from __future__ import annotations

import base64
import json
from functools import lru_cache
from io import BytesIO
from typing import Dict, List

import pygame


@lru_cache(maxsize=None)
def load_base64_png(path_txt: str) -> pygame.Surface:
    """Load a base64-encoded PNG text file into a ``Surface``.

    Parameters
    ----------
    path_txt:
        Path to ``*.png.txt`` file.
    """
    with open(path_txt, "r", encoding="utf-8") as f:
        b64_data = f.read()
    image_data = base64.b64decode(b64_data)
    return pygame.image.load(BytesIO(image_data)).convert_alpha()


def load_json(path: str) -> dict:
    """Load a JSON file relative to package root."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_sprite_sheet(def_json: str, path_txt: str) -> Dict[str, List[pygame.Surface]]:
    """Load sprite sheet according to definition JSON.

    Parameters
    ----------
    def_json:
        JSON path describing states with frame rects.
    path_txt:
        Base64-encoded sprite sheet image.
    """
    meta = load_json(def_json)
    sheet = load_base64_png(path_txt)
    sprites: Dict[str, List[pygame.Surface]] = {}
    for state, frames in meta.items():
        sprites[state] = []
        for x, y, w, h in frames:
            frame = pygame.Surface((w, h), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), pygame.Rect(x, y, w, h))
            sprites[state].append(frame)
    return sprites
