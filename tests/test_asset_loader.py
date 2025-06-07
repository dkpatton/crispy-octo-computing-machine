import pygame
import pytest

from emerson_game.core.asset_loader import load_base64_png


@pytest.mark.pygame
def test_load_base64_png_size(pygame_display):
    surf = load_base64_png('emerson_game/assets/sprites/hero_idle.png.txt')
    assert surf.get_size() == (16, 16)
