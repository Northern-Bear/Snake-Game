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
# space between each snake segment
segment_margin = 3

class Snake(pygame.sprite.Sprite):
    """ Player controlled Snake class """

    # ---- Methods ----#
    def __init__(self, x, y) -> None:
        """ Constructor Method """
        pygame.sprite.Sprite.__init__(self)

        # Set the height and width of snake 
        self.image = pygame.Surface([snake_width, snake_height])
        self.image.fill(WHITE)

        # Snake position
        self.rect = self.image.get_rect()    
        self.rect.x = x
        self.rect.y = y

        # Snake speed vector
        self.change_x = 0
        self.change_y = 0

    def change_direction(self, dir):
        # Changes the player direction
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
        # Add the movement to the snake position
        self.rect.x += self.change_x
        self.rect.y += self.change_y

def main():
    # Initialize pygame
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set the title of the window
    pygame.display.set_caption("Snake by Northern Bear")

    # Create a snake instance and add to snake group
    snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    snake_list = pygame.sprite.Group()
    snake_list.add(snake)

    clock = pygame.time.Clock()
    done = False

    """ -----Main Program Loop----- """
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Set the keyboard events for movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    snake.change_direction("left")
                elif event.key == pygame.K_d:
                    snake.change_direction("right")
                elif event.key == pygame.K_w:
                    snake.change_direction("up")
                elif event.key == pygame.K_s:
                    snake.change_direction("down")

        """ -----Game Logic----- """
        snake_list.update()

        """ -----Drawing Code----- """
        # Clear the screen
        screen.fill(BLACK)
        # Draw sprites
        snake_list.draw(screen)
        # Flip the screen
        pygame.display.flip()

        # set how many frames per second
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()