from abc import ABC, abstractmethod
from typing import Any
import pygame
import pygame.tests
from event_info import EventInfo
from entities import Rocky, Enemy
from random import choice
from button import Button
import json


class GameState(ABC):
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.is_over = False
        self.sky_surf = pygame.image.load("..\\assets\\background\\sky.png")

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
        
        self.font = pygame.font.Font("..\\assets\\other\\Freedom-10eM.ttf", 100)
        self.text_surf = self.font.render("This Rock's Got Lots O' Opps", True, "white")
        self.text_rect = self.text_surf.get_rect(midtop=(400, 100))
        self.text_velocity = -1
        
        self.play_button = Button("center", (400, 300), (400, 200), ("..\\assets\\play_button\\play_button.png", "..\\assets\\play_button\\play_button_while_hovering.png"))
    
    def update(self, event_info: EventInfo) -> None:
        self.play_button.update(event_info)
        if self.play_button.clicked:
            self.is_over = True
        
        self.text_rect.centery += self.text_velocity
        
        if self.text_rect.top <= 50 or self.text_rect.bottom >= 150:
            self.text_velocity = -self.text_velocity
    
    def next_game_state(self) -> Any:
        return Main_Game(self.screen)

    def draw(self) -> None:
        self.play_button.draw(self.screen)
        self.screen.blit(self.text_surf, self.text_rect)



class Main_Game(GameState):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.font = pygame.font.Font("..\\assets\\other\\Freedom-10eM.ttf", 50)

        self.dirt_surf = pygame.image.load("..\assets\\background\\dirt.png")
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
            elif sprite.rect.colliderect(self.player_rock.rect):
                self.is_over = True

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
        self.score = score
        self.score_font = pygame.font.Font("..\\assets\\other\\Freedom-10eM.ttf", 50)
        
        with open("data.json", "r") as data_json:
            data = json.load(data_json)
            self.high_score = data["high_score"]
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.json", "w") as data_json:
                json.dump({"high_score" : self.high_score}, data_json, indent=4)

        self.score_surf = self.score_font.render(f"Score: {self.score}", True, "white")
        self.score_rect = self.score_surf.get_rect(midbottom=(400, 225))
        
        if self.score == self.high_score:
            self.high_score_surf = self.score_font.render(f"NEW HIGH SCORE: {self.high_score}", True, "white")
        else:
            self.high_score_surf = self.score_font.render(f"High Score: {self.high_score}", True, "white")
        self.high_score_rect = self.high_score_surf.get_rect(midtop=(400, 225))

        self.play_again_button = Button("midtop", (400, 300), (0, 0), ("..\\assets\\play_button\\play_button.png", "..\\assets\\play_button\\play_button_while_hovering.png"))
