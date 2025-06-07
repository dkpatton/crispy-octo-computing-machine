"""Entry point to run Emerson's Game demo."""

from __future__ import annotations

import pygame

from emerson_game.core.camera import Camera
from emerson_game.core.constants import BG_COLOR, INTERNAL_SIZE
from emerson_game.core.input_manager import InputManager
from emerson_game.core.level_loader import LevelLoader
from emerson_game.core.physics_engine import PhysicsEngine


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(INTERNAL_SIZE, pygame.SCALED)
    clock = pygame.time.Clock()

    input_mgr = InputManager("emerson_game/data/control_config.json")
    level = LevelLoader.load("emerson_game/levels/level_1.json")
    physics = PhysicsEngine()
    camera = Camera(INTERNAL_SIZE, level.bounds)

    for ent in level.entities:
        physics.add(ent)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        input_mgr.process_events()
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                running = False

        physics.update(dt)
        for ent in level.entities:
            ent.update(dt, input_mgr)
        camera.update(level.player)
        screen.fill(BG_COLOR)
        level.draw(screen, camera)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
