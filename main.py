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

        self.change_x = 0
        self.change_y = 0

    def change_direction(self, dir):
        match dir:
            case "left":
                self.change_x = (snake_width + segment_margin) * -1
                self.change_y = 0
            case "right":
                self.change_x = (snake_width + segment_margin)
                self.change_y = 0
            case "up":
                self.change_x = 0
                self.change_y = (snake_height + segment_margin) * -1
            case "down":
                self.change_x = 0
                self.change_y = (snake_height + segment_margin)
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    snake.change_direction("left")
                elif event.key == pygame.K_d:
                    snake.change_direction("right")
                elif event.key == pygame.K_w:
                    snake.change_direction("up")
                elif event.key == pygame.K_s:
                    snake.change_direction("down")

        snake_list.update()                    

        screen.fill(BLACK)

        snake_list.draw(screen)

        pygame.display.flip()

        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()