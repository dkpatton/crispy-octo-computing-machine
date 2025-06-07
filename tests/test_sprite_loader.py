import json
from pathlib import Path

import pygame

from emerson_game.core.sprite_loader import SpriteLoader


def test_load_image(tmp_path: Path) -> None:
    pygame.init()
    surf = pygame.Surface((10, 10), pygame.SRCALPHA)
    img_path = tmp_path / "img.png"
    pygame.image.save(surf, img_path)
    loaded = SpriteLoader.load_image(str(img_path))
    assert isinstance(loaded, pygame.Surface)


def test_load_sheet(tmp_path: Path) -> None:
    pygame.init()
    sheet = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.image.save(sheet, tmp_path / "sheet.png")
    meta = {
        "sprite_sheet": str(tmp_path / "sheet.png"),
        "frames": {"idle": [[0, 0, 8, 8]]},
    }
    meta_path = tmp_path / "sheet.json"
    meta_path.write_text(json.dumps(meta))
    frames = SpriteLoader.load_sheet(str(meta_path))
    assert "idle" in frames
    assert isinstance(frames["idle"][0], pygame.Surface)


def test_load_grid(tmp_path: Path) -> None:
    pygame.init()
    meta = {
        "palette": ["#00000000", "#ff0000"],
        "grid": [
            "0110",
            "1111",
            "0110",
            "0000",
        ],
    }
    json_path = tmp_path / "sprite.png.json"
    json_path.write_text(json.dumps(meta))
    surface = SpriteLoader.load_image(str(tmp_path / "sprite.png"))
    assert surface.get_size() == (4, 4)
