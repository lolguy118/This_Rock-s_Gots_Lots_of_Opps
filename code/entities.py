import pygame
from event_info import EventInfo
import random


class Rocky(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.original_image = pygame.image.load("..\\assets\\rock\\rocky.png")
        self.original_image = pygame.transform.scale(self.original_image, (400, 200))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(75, 225))
        self.angle = 0

    def animate(self):
        self.angle -= 5
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def handle_input(self, event_info: EventInfo):
        events = event_info["events"]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.rect.centery >= 225:
                    self.rect.centery = self.rect.centery - 150
                elif event.key == pygame.K_DOWN and self.rect.centery <= 225:
                    self.rect.centery = self.rect.centery + 150

    def update(self, event_info: EventInfo):
        self.animate()
        self.handle_input(event_info)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type: str) -> None:
        super().__init__()
        self.type = type
        if self.type == "knife_rock":
            knife_rock_1 = pygame.image.load("..\\assets\\knife_rock\\knife_rock_1.png")
            knife_rock_2 = pygame.image.load("..\\assets\\knife_rock\\knife_rock_1.png")
            self.frames = [knife_rock_1, knife_rock_2]
        elif self.type == "fbi_missile":
            missile_fly_1 = pygame.image.load(
                "..\\assets\\fbi_missile\\missile_fly_1.png"
            )
            missile_fly_2 = pygame.image.load(
                "..\\assets\\fbi_missile\\missile_fly_2.png"
            )
            self.frames = [missile_fly_1, missile_fly_2]
        elif self.type == "egg":
            egg = pygame.image.load("..\\assets\\egg\\egg.png")
            self.frames = [egg]
        elif self.type == "bird":
            bird_fly_1 = pygame.image.load("..\\assets\\bird\\bird_fly_1.png")
            bird_fly_2 = pygame.image.load("..\\assets\\bird\\bird_fly_2.png")
            self.frames = [bird_fly_1, bird_fly_2]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            center=(random.randint(900, 1100), random.choice([75, 225, 375]))
        )

    def animate(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[self.animation_index]

    def update(self) -> None:
        self.animate()
        match self.type:
            case "knife_rock":
                self.rect.x -= 5
            case "fbi_missile":
                self.rect.x -= 40
            case "egg":
                self.rect.x -= 30
            case "bird":
                self.rect.x -= 20
        self.destroy()

    def destroy(self):
        if self.rect.right <= -10:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((800, 450))
rocky = pygame.sprite.GroupSingle(Rocky())

while True:
    events: EventInfo = {"events": pygame.event.get()}
    for event in events["events"]:
        if event.type == pygame.QUIT:
            raise SystemExit

    screen.fill("black")
    rocky.draw(screen)
    rocky.update(events)
    pygame.display.update()
