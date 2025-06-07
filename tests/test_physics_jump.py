import pygame
import pytest

from emerson_game.core.physics import Body, PhysicsEngine


@pytest.mark.pygame
def test_jump_physics(pygame_display):
    platforms = pygame.sprite.Group()
    engine = PhysicsEngine(platforms)
    body = Body(pygame.Rect(0, 0, 16, 16))
    body.vel_y = engine.JUMP_SPEED

    # simulate few frames
    prev_vel = body.vel_y
    for _ in range(10):
        engine.apply_gravity(body, 1/60)
        engine.move(body, 1/60)
        assert body.vel_y <= engine.TERMINAL_VELOCITY
    assert body.vel_y > prev_vel
