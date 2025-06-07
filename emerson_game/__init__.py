"""Entry point for Emerson's Game."""
from __future__ import annotations


def main() -> None:
    from . import main as game_main
    game_main.run()


if __name__ == "__main__":
    main()
