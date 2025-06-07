"""Main game loop for Emerson's Game."""
from __future__ import annotations

import pygame

from .core import settings
from .core.asset_loader import load_base64_png, load_json
from .core.input_manager import InputManager
from .core.physics import PhysicsEngine
from .core.level_loader import load_level
from .core.camera import Camera
from .entities.player import Player


def run() -> None:
    pygame.init()
    pygame.display.set_caption("Emerson's Game")
    window = pygame.display.set_mode((settings.SCREEN_WIDTH * 2, settings.SCREEN_HEIGHT * 2))
    screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    sprites_def = load_json('emerson_game/data/characters.json')
    hero_sprites = load_base64_png('emerson_game/assets/sprites/hero_idle.png.txt')
    hero_sheet = {'idle': [hero_sprites]}

    tileset_img = load_base64_png('emerson_game/assets/tilesets/ground_tiles.png.txt')

    level = load_level('emerson_game/data/levels/demo_level.json', tileset_img)
    player = Player(level.player_start, hero_sheet)
    physics = PhysicsEngine(level.platforms)
    input_bindings = load_json('emerson_game/data/input_bindings.json')
    input_mgr = InputManager(input_bindings)
    camera = Camera(pygame.Vector2(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                    pygame.Vector2(level.size[0] * settings.TILE_SIZE, level.size[1] * settings.TILE_SIZE),
                    pygame.Vector2(0, 0))

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(settings.FPS) / 1000.0
        input_mgr.process_events()
        input_mgr.update_continuous()

        player.update(dt, input_mgr.state)
        physics.apply_gravity(player.body, dt)
        physics.move(player.body, dt)
        player.rect = player.body.rect

        camera.update(player.rect)

        screen.fill((92, 148, 252))
        for tile in level.platforms:
            screen.blit(tile.image, camera.world_to_screen(tile.rect))
        screen.blit(player.image, camera.world_to_screen(player.rect))

        pygame.transform.scale(screen, window.get_size(), window)
        if settings.DEV_MODE:
            fps_text = pygame.font.SysFont(None, 20).render(str(int(clock.get_fps())), True, (255, 255, 255))
            window.blit(fps_text, (2, 2))
        pygame.display.flip()


if __name__ == '__main__':
    run()
