import pygame
import random

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
segment_margin = 1
# Height and width of food sprite
food_width = 15
food_height = 15

class Snake(pygame.sprite.Sprite):
    """ Player controlled Snake class """

    # ---- Methods ----#
    def __init__(self, x, y) -> None:
        """ Constructor Method """
        super().__init__()

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
                self.change_x = (snake_width) * -1
                self.change_y = 0
            case "right":
                self.change_x = (snake_width)
                self.change_y = 0
            case "up":
                self.change_x = 0
                self.change_y = (snake_height) * -1
            case "down":
                self.change_x = 0
                self.change_y = (snake_height)
 
    def update(self):
        # Add the movement to the snake position
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        print(self.rect.x, self.rect.y)

    def check_collision(self, food, collision_group, segment_list, draw_group):

        blocks_hit_list = pygame.sprite.spritecollide(self, collision_group, True)
    
        # Check the list of collisions.
        for block in blocks_hit_list:

            # Create new snake segment
            segment = Snake(self.rect.x, self.rect.y)
            segment_list.append(segment)
            draw_group.add(segment)

            food.change_pos()
            collision_group.add(food)
            draw_group.add(food)

class Food(pygame.sprite.Sprite):
    """ Food class """

    # ---- Methods ---- #
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface([food_width, food_height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200
    
    def change_pos(self):
        self.rect.x = random.randrange(0, SCREEN_WIDTH, snake_width)
        self.rect.y = random.randrange(0, SCREEN_HEIGHT, snake_height)
        print(self.rect.x, self.rect.y)

def main():
    # Initialize pygame
    pygame.init()

    # Game variables
    score = 0

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set the title of the window
    pygame.display.set_caption("Snake by Northern Bear")

    # Create Groups for sprites
    food_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()

    # Create a snake instance and add to draw group
    snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites_list.add(snake)
    # Empty list to hold size of snake
    snake_segments = []
    snake_segments.append(snake)

    # Create food object and add to food group and draw group
    food = Food()
    food_list.add(food)
    all_sprites_list.add(food)

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
        snake.update()

        # See if the snake object has collided with food object.
        snake.check_collision( food, food_list, snake_segments, all_sprites_list)

        # Check if there is more than 1 segment
        if len(snake_segments) > 1:

            # Remove last segment
            old_segment = snake_segments.pop()
            all_sprites_list.remove(old_segment)

            # determine where to create new segment
            segment_x = snake_segments[0].rect.x + (snake.change_x)
            segment_y = snake_segments[0].rect.y + (snake.change_y)
            segment = Snake(segment_x, segment_y)

            # Add to list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        """ -----Drawing Code----- """
        # Clear the screen
        screen.fill(BLACK)

        # Draw sprites
        all_sprites_list.draw(screen)

        for i in range(0, SCREEN_WIDTH - 1, snake_width):
            for j in range(0, SCREEN_HEIGHT - 1, snake_height):
                pygame.draw.rect(screen, WHITE, [i,  j, snake_width, snake_height], 1)
                
            

        # Flip the screen
        pygame.display.flip()

        # set how many frames per second
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()