# Modules 
import pygame.sprite
from settings import *

class Fighter(pygame.sprite.Sprite):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        super().__init__()
        self.player = player # Player 1 (left) or 2 (right)
        self.size = data[0] # Sprite size
        self.image_scale = data[1] # Scaling
        self.offset = data[2] # Image offset to get the right position
        self.flip = flip # Flip iamge to make sure fighters face each other
        self.animation_list = self.load_images(sprite_sheet, animation_steps) # Animation from spritesheet
        self.action = 0  # 0: idle #1: run #2: jump #3: attack1 #4: attack2 #5: hit #6: death
        self.frame_index = 0 # Animation frame 
        self.image = self.animation_list[self.action][self.frame_index] # Image displayed based on animation frame and action
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) # Hitbox
        self.vel_y = 0 # movement value in y axis
        self.running = False 
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        # Get seperate images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Get keypresses
        key = pygame.key.get_pressed()

        # Allow other actions if not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            # Player 1 controls
            if self.player == 1:
                # Move
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_q] or key[pygame.K_e]:
                    # Attack type
                    if key[pygame.K_q]:
                        self.attack_type = 1
                        self.__attack(target)
                    if key[pygame.K_e]:
                        self.attack_type = 2
                        self.__attack(target)

            # Player 2 controls
            if self.player == 2:
                # Move
                if key[pygame.K_j]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_l]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_i] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_u] or key[pygame.K_o]:
                    # Attack type
                    if key[pygame.K_u]:
                        self.attack_type = 1
                        self.__attack(target)
                    if key[pygame.K_o]:
                        self.attack_type = 2
                        self.__attack(target)

        # Gravity
        self.vel_y += GRAVITY # Constant downward position change
        dy += self.vel_y

        # Limit player position within screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 70:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 70 - self.rect.bottom

        # Ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    # Animation updates
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6: Death
        elif self.hit:
            self.update_action(5)  # 5: Hit
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)  # 3: Attack1
            elif self.attack_type == 2:
                self.update_action(4)  # 4: Attack2
        elif self.jump:
            self.update_action(2)  # 2: Jump
        elif self.running:
            self.update_action(1)  # 1: Run
        else:
            self.update_action(0)  # 0: Idle

        animation_cooldown = 60 # duration of each frame
        # Update fighter image
        self.image = self.animation_list[self.action][self.frame_index]
        # Change to next frame after cooldown
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if the animation sequence has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # If fighter is dead then end the animation
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Check if an attack was executed
                if self.action == 3:
                    self.attacking = False
                    self.attack_cooldown = 20
                elif self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 45
                # Check if damage was taken
                if self.action == 5:
                    self.hit = False
                    # If the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 30

    def __attack(self, target):
        if self.attack_cooldown == 0:
            # Execute an attack
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if self.attack_type == 1:
                if attacking_rect.colliderect(target.rect):
                    target.health -= 10
                    target.hit = True
            elif self.attack_type == 2:
                if attacking_rect.colliderect(target.rect):
                    target.health -= 20
                    target.hit = True

    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
