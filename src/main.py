import pygame

from constants import BASE_PATH, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from lib.tilemap_renderer import TilemapRenderer


class Game:
    def __init__(self, **kwargs) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.clock = pygame.Clock()

        self.offset = pygame.Vector2(0, 0)

        self.running = True

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        speed = 4
        move = pygame.Vector2(0, 0)

        if keys[pygame.K_LEFT]:
            move.x -= speed
        if keys[pygame.K_RIGHT]:
            move.x += speed
        if keys[pygame.K_UP]:
            move.y -= speed
        if keys[pygame.K_DOWN]:
            move.y += speed

        self.offset += move

    def update(self):
        self.handle_event()

    def run(self):
        tilemap = TilemapRenderer()
        tilemap.load_map(BASE_PATH / "map" / "0.json")
        while self.running:
            self.update()
            self.screen.fill((0, 0, 0, 0))
            tilemap.render_tiles(self.screen, self.offset)
            self.clock.tick(FPS)
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
