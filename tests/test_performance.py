import os
import pygame

from emerson_game.core.camera import Camera
from emerson_game.core.constants import BG_COLOR, INTERNAL_SIZE
from emerson_game.core.input_manager import InputManager
from emerson_game.core.level_loader import LevelLoader
from emerson_game.core.physics_engine import PhysicsEngine


def test_headless_fps() -> None:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.display.init()
    screen = pygame.display.set_mode(INTERNAL_SIZE, pygame.HIDDEN)
    clock = pygame.time.Clock()

    input_mgr = InputManager("emerson_game/data/control_config.json")
    level = LevelLoader.load("emerson_game/levels/level_1.json")
    physics = PhysicsEngine()
    camera = Camera(INTERNAL_SIZE, level.bounds)

    for ent in level.entities:
        physics.add(ent)

    start = pygame.time.get_ticks()
    for _ in range(120):
        dt = clock.tick(60) / 1000.0
        input_mgr.process_events()
        physics.update(dt)
        for ent in level.entities:
            ent.update(dt, input_mgr)
        camera.update(level.player)
        screen.fill(BG_COLOR)

    end = pygame.time.get_ticks()
    avg_fps = 120 / ((end - start) / 1000.0)
    assert avg_fps >= 50
    pygame.display.quit()
