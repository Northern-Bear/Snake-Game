import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Constant variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Player width and height of each segment
snake_width = 20
snake_height = 20
segment_margin = 3

class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([snake_width, snake_height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()    

        self.rect.x = x
        self.rect.y = y  

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake by Northern Bear")

    snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    snake_list = pygame.sprite.Group()
    snake_list.add(snake)

    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)

        snake_list.draw(screen)

        pygame.display.flip()

        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()