import pygame
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Constant variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CELL_WIDTH = 20
CELL_HEIGHT = 20

# space between each snake segment
segment_margin = 1

class PlayArea(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.area_width = 600
        self.area_height = 600

        self.image = pygame.Surface([self.area_width, self.area_height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 0


class Snake(pygame.sprite.Sprite):
    """ Player controlled Snake class """

    # ---- Methods ----#
    def __init__(self, x, y) -> None:
        """ Constructor Method """
        super().__init__()

        # Player width and height of each segment
        self.snake_width = 20
        self.snake_height = 20

        # Set the height and width of snake 
        self.image = pygame.Surface([self.snake_width, self.snake_height])
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
                self.change_x = (self.snake_width) * -1
                self.change_y = 0
            case "right":
                self.change_x = (self.snake_width)
                self.change_y = 0
            case "up":
                self.change_x = 0
                self.change_y = (self.snake_height) * -1
            case "down":
                self.change_x = 0
                self.change_y = (self.snake_height)
 
    def update(self):
        # Add the movement to the snake position
        self.rect.x += self.change_x
        self.rect.y += self.change_y


class Food(pygame.sprite.Sprite):
    """ Food class """

    # ---- Methods ---- #
    def __init__(self) -> None:
        """ Constructor Method """
        super().__init__()

        self.screen = PlayArea()

        # Height and width of food sprite
        self.food_width = 15
        self.food_height = 15

        self.image = pygame.Surface([self.food_width, self.food_height])
        self.image.fill(WHITE)

        # Position of food object
        self.rect = self.image.get_rect()
        self.rect.x = 240
        self.rect.y = 200
    
    def change_pos(self):
        # Changes the pos of food before drawring again.
        self.rect.x = random.randrange(self.screen.rect.x, self.screen.area_width - self.food_width, CELL_WIDTH)
        self.rect.y = random.randrange(self.screen.rect.y, self.screen.area_height - self.food_height, CELL_HEIGHT)


class Game(object):
    def __init__(self) -> None:
        
        # Game variables
        self.score = 0
        self.game_over = False

        # Create Groups for sprites
        self.food_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        # create play area
        self.play_area = PlayArea()
        # Create a snake instance and add to draw group
        self.snake = Snake(self.play_area.area_width // 2, self.play_area.area_height // 2)
        self.all_sprites_list.add(self.snake)
        # Empty list to hold size of snake
        self.snake_segments = []
        self.snake_segments.append(self.snake)
        # Create food object and add to food group and draw group
        self.food = Food()
        self.food_list.add(self.food)
        self.all_sprites_list.add(self.food)
        # Select the font to use, size, bold, italics
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.title_text = self.font.render("-- SNAKE --", True, WHITE)
        self.game_over_text = self.font.render(" Game Over. Please press 'r' to restart ", True, WHITE)
        

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # Set the keyboard events for movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.snake.change_direction("left")
                elif event.key == pygame.K_d:
                    self.snake.change_direction("right")
                elif event.key == pygame.K_w:
                    self.snake.change_direction("up")
                elif event.key == pygame.K_s:
                    self.snake.change_direction("down")
                
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.__init__()

    def run_logic(self):
            
            if not self.game_over:

                self.snake.update()

                # See if the snake object has collided with food object.
                self.check_collision()
                # Check if there is more than 1 segment
                if len(self.snake_segments) > 1:

                    # Remove last segment
                    old_segment = self.snake_segments.pop()
                    self.all_sprites_list.remove(old_segment)

                    # determine where to create new segment
                    segment_x = self.snake_segments[0].rect.x + (self.snake.change_x)
                    segment_y = self.snake_segments[0].rect.y + (self.snake.change_y)
                    segment = Snake(segment_x, segment_y)

                    # Add to list
                    self.snake_segments.insert(0, segment)
                    self.all_sprites_list.add(segment)
                    self.snake.rect.x = self.snake_segments[0].rect.x
                    self.snake.rect.y = self.snake_segments[0].rect.y

                if self.snake.rect.x < self.play_area.rect.x or self.snake.rect.x > self.play_area.rect.x + self.play_area.area_width:
                    self.game_over = True
                elif self.snake.rect.y < self.play_area.rect.y or self.snake.rect.y > self.play_area.rect.y + self.play_area.area_height:
                    self.game_over = True
                else:
                    self.game_over = False
    
    def check_collision(self):

        blocks_hit_list = pygame.sprite.spritecollide(self.snake, self.food_list, True)
    
        # Check the list of collisions.
        for block in blocks_hit_list:
            self.score += 1

            # Create new snake segment
            segment = Snake(self.snake.rect.x, self.snake.rect.y)
            self.snake_segments.append(segment)
            self.all_sprites_list.add(segment)

            self.food.change_pos()
            self.food_list.add(self.food)
            self.all_sprites_list.add(self.food)

            print(self.score)

    def display_frame(self, screen):
        # Clear the screen
        screen.fill(BLACK)

        self.score_text = self.font.render("Score: " + str(self.score), True, WHITE)

        if self.game_over:

            screen.blit(self.game_over_text, [200, 240])

        # Draw sprites
        if not self.game_over:

            screen.blit(self.title_text, [40, 5])
            screen.blit(self.score_text, [5, 30])
            self.all_sprites_list.draw(screen)

            pygame.draw.rect(screen, WHITE, [self.play_area.rect.x,  self.play_area.rect.y, self.play_area.area_width, self.play_area.area_height], 1)
                
        # Flip the screen
        pygame.display.flip()

                
def main():

    # Initialize pygame
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set the title of the window
    pygame.display.set_caption("Snake by Northern Bear")

    clock = pygame.time.Clock()
    done = False

    game = Game()

    """ -----Main Program Loop----- """
    while not done:
        done = game.process_events()

        """ -----Game Logic----- """
        game.run_logic()

        """ -----Drawing Code----- """
        game.display_frame(screen)
        # set how many frames per second
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()