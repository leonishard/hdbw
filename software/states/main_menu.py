import sys
import pygame, random
import button
from pygame.math import Vector2
from pygame import mixer

#pygame setup
pygame.init()

#screen setup
cell_size = 40
cell_number = 20

#screen_heith = 600
#screen_width = 800
#display size
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("schlangen spiel")
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 25)

#Game State Setup
states = {
    1:"Menu",
    2:"Game",
    3:"game_over",
    4:"options"
}
#defining the starting game state
game_state = states[1]

#loading button images
start_img = pygame.image.load("../start_image.png").convert_alpha()
exit_img = pygame.image.load("../exit_image.png").convert_alpha()
main_menu_img = pygame.image.load("../main_menu_img.png")
options_img = pygame.image.load("../pixil-frame-0.png").convert_alpha()
snake_img = pygame.image.load("../snake_img.png").convert_alpha()

options_menu_img = pygame.image.load("../options menu.png").convert_alpha()
back_img = pygame.image.load("../back_img.png").convert_alpha()
volume_img = pygame.image.load("../music_img.png").convert_alpha()
game_difficulty_img = pygame.image.load("../game_diff.png").convert_alpha()
how_hard_img = pygame.image.load("../how_hard.png").convert_alpha()

easy_diff_img = pygame.image.load("../game_diff.png").convert_alpha()
med_diff_img = pygame.image.load("../med_diff_img.png").convert_alpha()
hard_diff_img = pygame.image.load("../hard_diff_img.png").convert_alpha()
impos_diff_img = pygame.image.load("../impos_diff_img.png").convert_alpha()


#drawing button on screen
#main screen buttons and picture of snake
start_button = button.Button(80, 350, start_img,1.2)
exit_button = button.Button(480, 350, exit_img,1.2)
options_button = button.Button(280, 550, options_img, 1.2)
snake_real = button.Button(10,500,snake_img,2.5)

#options menu buttons
back_button = button.Button(190, 600, back_img, 1)
volume_button = button.Button(190,450,volume_img,1)
game_diff_button = button.Button(190, 300, game_difficulty_img, 1)

#titles of the main menu options and the difficutly scale
options_menu_title = button.Button(150, 50, options_menu_img, 2.5)
main_menu_title = button.Button(150, 50, main_menu_img, 2.5)
how_hard_title = button.Button(400, 310, how_hard_img, 2.5)

#adding music
mixer.music.load("../gute_music.mp3")
mixer.music.play(-1)


#creating the fruit
class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        #making the fruit as big as a cell
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (pygame.Color("red")), fruit_rect)

    def randomize(self):
        #placing the fruit on a random cell and making sure that it is one the screen
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

#creating snake
class SNAKE:
    def __init__(self):
        #starting postions for the snake
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(pygame.Color("green")), block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

#this is where everything is check (collisions, fails, the refreshrate)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        #updates the game
        self.snake.move_snake()
        self.check_collisions()
        self.check_fail()

    def draw_elements(self):
        #draws elemnts on the screen
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collisions(self):
        #checks if the snake and the furit have collided
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        #checking if the head of the snake has hit any of the walls this checks if snake is between 0 and the number of cell sizes
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        #if snake hits it self
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (pygame.Color("white")))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y ))
        screen.blit(score_surface, score_rect)
main_game = MAIN()


#game difficulty due to the game speed how many milliseconds it takes for the screen to update
game_speed = 160

#creating a timer on when to update the snakes movment
SCREEN_UPDATE = pygame.USEREVENT

#game speed
pygame.time.set_timer(SCREEN_UPDATE, game_speed)


#while loop to creat game states
run = True
while run:

    #Menu Logic
    if game_state == "Menu":
        screen.fill((100, 100, 150))

        #visual buttons
        main_menu_title.draw(screen)
        snake_real.draw(screen)

        #functional buttons
        if start_button.draw(screen):
            game_state = states[2]

        if exit_button.draw(screen):
            run = False
            sys.exit()

        if options_button.draw(screen):
            game_state = states[4]

        #see if game is closed
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()

    # Game Logic
    if game_state == "Game":
        #seaches for imputs to cole game
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == SCREEN_UPDATE:
                main_game.update()

            #movment of the snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction[1] != 1:
                        main_game.snake.direction = (0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction[1] != -1:
                        main_game.snake.direction = (0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction[0] != 1:
                        main_game.snake.direction = (-1,0)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction[0] != -1:
                        main_game.snake.direction = (1,0)

                if event.key == pygame.K_ESCAPE:
                    game_state = states[1]


        screen.fill(pygame.Color("blue"))
        main_game.draw_elements()

    # options logic
    if game_state == "options":

        screen.fill((178, 190, 181))

        # title of the options menu
        options_menu_title.draw(screen)

        # showing what the colors mean
        how_hard_title.draw(screen)

        # back button
        if back_button.draw(screen):
            game_state = states[1]

        #controling game speed
        if game_diff_button.draw(screen):
            if game_speed <= 10:
                game_speed = 160

            else:
                game_speed -= 50

            # changing the game difficulty
            print(game_speed)
            pygame.time.set_timer(SCREEN_UPDATE, game_speed)
            if game_speed == 160:
                game_diff_button.setImage(easy_diff_img, 1)
            elif game_speed == 110:
                game_diff_button.setImage(med_diff_img, 1)
            elif game_speed == 60:
                game_diff_button.setImage(hard_diff_img, 1)
            elif game_speed == 10:
                game_diff_button.setImage(impos_diff_img, 1)

        #turing the music on and of
        if volume_button.draw(screen):
            if mixer.music.get_busy():
                mixer.music.pause()
            else:
                mixer.music.unpause()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

    pygame.display.update()
    clock.tick(60)
