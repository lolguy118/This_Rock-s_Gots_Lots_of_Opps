import pygame
from coordinate import Coordinate
from typing import Tuple
from event_info import EventInfo
class Button:
    def __init__(self, position_used_to_place : str, xy : Coordinate, width_and_height : Coordinate, images_paths : Tuple[str, str]) -> None:
        self.pos_used_to_place = position_used_to_place
        self.xy = xy
        self.width_and_height = width_and_height
        self.images = images_paths
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect()
        self.rectangle_get()

        self.hover = False
        self.clicked = False
    def rectangle_get(self) -> None:
        match self.pos_used_to_place:
            case "center":
                self.rect.center = self.xy
            case "topleft":
                self.rect.topleft = self.xy
            case "topright":
                self.rect.topright = self.xy
            case "midright":
                self.rect.midright = self.xy
            case "bottomright":
                self.rect.bottomright = self.xy
            case "midbottom":
                self.rect.midbottom = self.xy
            case "bottomleft":
                self.rect.bottomleft = self.xy
            case "midleft":
                self.rect.midleft = self.xy
    
    def update(self, event_info : EventInfo) -> None:
        mouse_pos = event_info["mouse_pos"]
        events = event_info["events"]
        self.hover = self.rect.collidepoint(mouse_pos)
        
        if self.hover:
            self.image = pygame.image.load(self.images[1])
        else:
            self.image = pygame.image.load(self.images[0])
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.hover:
                self.clicked = True
    
    def draw(self, screen : pygame.Surface):
        screen.blit(self.image, self.rect)