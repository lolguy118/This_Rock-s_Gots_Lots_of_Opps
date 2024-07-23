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
    def __init__(self, screen: pygame.Surface, start_time: int) -> None:
        super().__init__(screen)

        self.font = pygame.font.Font("..\\assets\\other\\Freedom-10eM.ttf", 50)

        self.sky_surf = pygame.image.load("..\\assets\\other\\sky.png")

        self.dirt_surf = pygame.image.load("..\assets\\other\\dirt.png")
        self.upper_dirt_rect = self.dirt_surf.get_rect(bottomright=(0, 150))
        self.middle_dirt_rect = self.dirt_surf.get_rect(bottomright=(0, 300))
        self.lower_dirt_rect = self.dirt_surf.get_rect(bottomright=(0, 450))

        self.player_rock = Rocky()
        self.player_group = pygame.sprite.GroupSingle(self.player_rock)
        self.enemies = pygame.sprite.Group()

        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 1500)
        self.score = 0

    def update_score(self):
        for sprite in self.enemies:
            if sprite.rect.left == 0:
                self.score += 1

    def update(self, event_info: EventInfo) -> None:
        events = event_info["events"]
        for event in events:
            if event.type == self.enemy_timer:
                self.enemies.add(
                    Enemy(choice(["knife_rock", "fbi_missile", "egg", "bird"]))
                )
        self.enemies.update()
        self.player_group.update(event_info)
        self.update_score()

    def draw(self) -> None:
        self.score_text_surf = self.font.render(str(self.score), True, "white")
        self.score_text_rect = self.score_text_surf.get_rect(midtop=(400, 0))
        self.screen.blit(self.sky_surf, (0, 0))
        self.screen.blit(self.dirt_surf, self.upper_dirt_rect)
        self.screen.blit(self.dirt_surf, self.middle_dirt_rect)
        self.screen.blit(self.dirt_surf, self.lower_dirt_rect)
        self.enemies.draw(self.screen)
        self.player_group.draw(self.screen)

    def next_game_state(self) -> Any:
        return Play_Again_Screen(self.screen, self.score)


class Play_Again_Screen(GameState):
    def __init__(self, screen: pygame.Surface, score: int) -> None:
        super().__init__(screen)
