from abc import ABC, abstractmethod
from typing import Any
import pygame
from event_info import EventInfo
from entities import Rocky, Enemy
from random import choice


class GameState(ABC):
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.is_over = False
        self.board_surf = pygame.image.load("..\\assets\\Board.png")

    @abstractmethod
    def update(self, event_info: EventInfo) -> None:
        pass

    @abstractmethod
    def next_game_state(self) -> Any:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

class Title_Screen(GameState):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

class Game(GameState):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

class Play_Again_Screen(GameState):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.player_rock = Rocky()
        self.enemies = []