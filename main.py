import pygame as pg
from fighter import Fighter

pg.init()

# sets the frame rate of the game to suit all computers.
clock = pg.time.Clock()
fps = 60

# window size.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# sets the display size of the game.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# sets the name on the bar of the game.
pg.display.set_caption('Test')

# loading background images.
background_img = pg.image.load('C:/Users/user/PycharmProjects/training_project/assets/background/background.jpg').convert_alpha()
# background_img = pg.transform.scale(background_img,(background_img.get_width()*2.4,background_img.get_height() * 2.7))
###############################################################################################
###############################################################################################

# define fighter variables.
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load spreadsheets.
warrior_sheet = pg.image.load('C:/Users/user/PycharmProjects/training_project/assets/warrior/warrior.png').convert_alpha()
wizard_sheet = pg.image.load('C:/Users/user/PycharmProjects/training_project/assets/wizard/wizard.png').convert_alpha()

# number of frames in each animation.
WARRIOR_ANIMATION_FRAMES = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_FRAMES = [8, 8, 1, 8, 8, 3, 7]


# function for drawing background.
def draw_bg():
    scaled_bg = pg.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


############################################################################################
############################################################################################
############################################################################################
#############################################################################################
############################################################################################
############################################################################################


# creating objects of class.
fighter_1 = Fighter(200, 100,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_FRAMES)
fighter_2 = Fighter(700, 100,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_FRAMES)


active = True

############################################################################################
############################################################################################
############################################################################################
# controls the boot of the game.
while active:

    # calling the set frame rate function.
    clock.tick(fps)

    # calling the draw background function.
    draw_bg()

    # move players.
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT)

    # draw players.
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # update fighters.
    fighter_1.update()
    fighter_2.update()
    # get the event from event handler func in pygame module.
    # if the event is "QUIT", it stops running the game.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            active = False

    # updates the display of the game.
    pg.display.update()
############################################################################################
############################################################################################
############################################################################################

pg.quit()