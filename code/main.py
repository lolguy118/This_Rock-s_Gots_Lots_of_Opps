import pygame
from states import Title_Screen
import states


class Game:

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 450
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    FPS_CAP = 60
    CLOCK = pygame.time.Clock()

    def __init__(self) -> None:
        self.current_game_state = Title_Screen(self.SCREEN)

    def get_events(self) -> dict:
        return {"events": pygame.event.get(), "mouse_pos": pygame.mouse.get_pos()}

    def run(self) -> None:
        while True:
            event_info = self.get_events()
            for event in event_info["events"]:
                if event.type == pygame.QUIT:
                    raise SystemExit

            self.SCREEN.fill("black")

            self.current_game_state.update(event_info)

            if self.current_game_state.is_over:
                self.current_game_state = self.current_game_state.next_game_state()

            self.current_game_state.draw()
            
            pygame.display.update()
            self.CLOCK.tick(self.FPS_CAP)


if __name__ == "__main__":
    game = Game()
    game.run()
