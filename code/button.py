import pygame
from coordinate import Coordinate
from typing import Tuple
from event_info import EventInfo
class Button:
    def __init__(self, position_used_to_place : str, xy : Coordinate, width_and_height : Coordinate, images_paths : Tuple[str, str]) -> None:
        self.pos_used_to_place = position_used_to_place
        self.x, self.y = xy
        self.width_and_height = width_and_height
        self.normal_image = pygame.image.load(images_paths[0]).convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, self.width_and_height)
        self.hovering_image = pygame.image.load(images_paths[1]).convert_alpha()
        self.hovering_image = pygame.transform.scale(self.hovering_image, self.width_and_height)
        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect()
        self.rectangle_get()

        self.hover = False
        self.clicked = False
    def rectangle_get(self) -> None:
        setattr(self.rect, self.pos_used_to_place, (self.x, self.y))
        print(f"Button rect: {self.rect}, Image size: {self.current_image.get_size()}")
    
    def update(self, event_info : EventInfo) -> None:
        mouse_pos = event_info["mouse_pos"]
        events = event_info["events"]
        self.hover = self.rect.collidepoint(mouse_pos)
        
        if self.hover:
            print("ok")
            self.current_image = self.hovering_image

        else:
            self.current_image = self.normal_image

        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.hover:
                self.clicked = True
    
    def draw(self, screen : pygame.Surface):
        screen.blit(self.current_image, self.rect)
        pygame.draw.rect(screen, "white", self.rect, width=1)