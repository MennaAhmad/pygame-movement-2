import pygame as pg
import pygame.time


class Fighter:
    def __init__(self, player, flip, x, y, data, sprite_sheet, animation_steps):
        self.rect = pg.Rect((x, y, 80, 180))
        self.size = data[0]  # stores the size values of the character.
        self.image_scale = data[1]  # stores the scale values of the character.
        self.offset = data[2]  # stores the offset values of the character.
        self.animation_list = self.load_images(sprite_sheet,
                                               animation_steps)  # a list of lists which loades the "whole" sprite sheet of the character, and the number of frames in each animation.
        self.frame_index = 0  # stores the index of the frame required in the sequence.
        self.action = 0  # a variable used to define the type of action. 0: Idle, 1:run,  2:jump,  3: attack 1, 4:attack 2, 5: damaged, 6:death.
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pg.time.get_ticks()  # stores the clock time.
        self.vel_y = 0
        self.running = False  # stores the running state.
        self.jump = False  # stores the jumping state.
        self.attack_type = 0  # stores the type of attack.
        self.attacking = False
        self.attack_cooldown = 0
        self.player = player
        self.flip = flip
        self.hit=False
        self.health = 100
        self.score = 0

    # loads the images into a list and scales them up.
    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0  # the change in x coordinates.
        dy = 0  # the change in y coordinates.
        self.running = False
        self.attack_type = 0

        ########################################################################################
        ########################################################################################
        # get Keypresses.
        key = pg.key.get_pressed()
        # movement horizontal.
        # move left.

        if self.attacking == False and self.health > 0:
            if self.player == 1:
                if key[pg.K_a]:
                    dx = -SPEED
                    self.running = True
                # move right.
                if key[pg.K_d]:
                    dx = SPEED
                    self.running = True
                # moving vertical.
                if key[pg.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                    # attack
                if key[pg.K_r] or key[pg.K_t]:
                    self.attack(target)
                # determine which attack type was used
                if key[pg.K_r]:
                    self.attack_type = 1
                if key[pg.K_t]:
                    self.attack_type = 2

            if self.player == 2:
                if key[pg.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                # move right.
                if key[pg.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # moving vertical.
                if key[pg.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pg.K_KP1] or key[pg.K_KP2]:
                    self.attack(target)
                # determine which attack type was used
                if key[pg.K_KP1]:
                    self.attack_type = 1
                if key[pg.K_KP2]:
                    self.attack_type = 2

        ########################################################################################
        ########################################################################################
        # apply Gravity.
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen.
        # left boundry.
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        # right boundry.
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        # top and bottom boundry.
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # update player position.
        self.rect.x += dx
        self.rect.y += dy

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

    def attack(self, target):
        if self.attack_cooldown == 0:
            # execute attack
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
        # attacking_rect = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)

    def update(self):
        # check what action player is performing.
        if self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # state attack 1
            elif self.attack_type == 2:
                self.update_action(4)  # state attack 2
        elif self.jump == True:
            self.update_action(2)  # jumping state.
        elif self.running == True:
            self.update_action(1)  # running state.
        else:
            self.update_action(0)  # idle state.

        # a variable to set the time between updating each frame.
        animation_cooldown = 50
        # updates the image.
        self.image = self.animation_list[self.action][self.frame_index]
        # checks if enough time has passed.
        if pg.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        # check if animation is finished.
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            # check if an attack excuted
            if self.action == 3 or self.action == 4:
                self.attacking = False

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # draws the players.
    def draw(self, surface):
        self.image = pg.transform.flip(self.image, self.flip, False)
        surface.blit(self.image, (
        self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
