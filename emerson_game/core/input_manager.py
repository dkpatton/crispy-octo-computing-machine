"""Keyboard and joystick input handling."""

from __future__ import annotations

import json
import pygame


class InputManager:
    """Translate pygame events into action flags."""

    def __init__(self, config_path: str):
        with open(config_path) as fh:
            cfg = json.load(fh)
        self._cfg = cfg
        self.left = False
        self.right = False
        self.jump = False
        self.attack = False
        self._joysticks = []
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            self._joysticks.append(pygame.joystick.Joystick(i))
            self._joysticks[-1].init()

    def process_events(self) -> None:
        """Update action flags based on input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == self._cfg["quit"]:
                    self._quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == self._cfg["joy_quit"]:
                    self._quit()

        keys = pygame.key.get_pressed()
        self.left = keys[self._cfg["left"]]
        self.right = keys[self._cfg["right"]]
        self.jump = keys[self._cfg["jump"]]
        self.attack = keys[self._cfg["attack"]]

        if self._joysticks:
            joy = self._joysticks[0]
            axis_x = joy.get_axis(self._cfg["joy_axis_x"])
            hat_x = joy.get_hat(0)[0]
            self.left |= axis_x < -0.5 or hat_x < 0
            self.right |= axis_x > 0.5 or hat_x > 0
            self.jump |= joy.get_button(self._cfg["joy_jump"])
            self.attack |= joy.get_button(self._cfg["joy_attack"])

    def _quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
