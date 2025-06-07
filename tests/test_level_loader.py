from emerson_game.core.level_loader import LevelLoader


def test_level_loader() -> None:
    level = LevelLoader.load("emerson_game/levels/level_1.json")
    assert level.width == 10
    assert level.player is not None
    assert len(level.entities) >= 1
