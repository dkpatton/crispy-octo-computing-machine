import pygame

from emerson_game.core.physics_engine import PhysicsEngine, PhysicsEntity


def test_collision_resolution() -> None:
    engine = PhysicsEngine()
    entity = PhysicsEntity()
    entity.rect = pygame.Rect(0, 0, 32, 32)
    ground = pygame.Rect(0, 40, 64, 16)
    engine.add(entity)
    engine.add_collider(ground)

    engine.update(0.1)
    assert entity.rect.bottom <= ground.top
