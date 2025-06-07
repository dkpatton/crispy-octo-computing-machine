"""Handle keyboard and game-pad input."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pygame


@dataclass
class InputState:
    move_x: int = 0
    jump: bool = False
    attack: bool = False


class InputManager:
    """Translate Pygame events into high-level actions."""

    def __init__(self, bindings: Dict[str, int]) -> None:
        self.bindings = bindings
        self.state = InputState()

    def process_events(self) -> None:
        self.state = InputState()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self._handle_keyboard(event)

    def _handle_keyboard(self, event: pygame.event.Event) -> None:
        pressed = event.type == pygame.KEYDOWN
        for action, key in self.bindings.items():
            if event.key == key:
                setattr(self.state, action, pressed if action != 'move_x' else (1 if pressed else 0))

    def update_continuous(self) -> None:
        keys = pygame.key.get_pressed()
        left = keys[self.bindings.get('left', pygame.K_LEFT)]
        right = keys[self.bindings.get('right', pygame.K_RIGHT)]
        self.state.move_x = right - left
        self.state.jump |= keys[self.bindings.get('jump', pygame.K_z)]
