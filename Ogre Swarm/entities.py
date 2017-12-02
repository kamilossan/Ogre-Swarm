import pygame
import textures
import random

# object lists to reference in game
global objects
global characters
objects = []
characters = []


# basic object type
class Object(pygame.sprite.Sprite):
    ##defaults, assign Rect as a hitbox
    collider = (0, 0, 0, 0)
    movement = [0, 0]
    out_of_bounds = False

    def __init__(self, position, sprite, screen):
        self.screen = screen
        self.movement = [0, 0]
        self.position = position
        self.sprite = pygame.Surface.copy(sprite)
        self.rect = self.sprite.get_rect()

        objects.append(self)
        self.draw()

    def draw(self):
        self.screen.blit(self.sprite, self.position)

    def update(self):
        self.displace()

    # call every frame to update position along with hitbox
    def displace(self):
        ##apply acceleration
        self.rect.topleft = (self.position[0], self.position[1])
        if not self.movement == [0, 0]:
            self.position[0] += self.movement[0]

            self.position[1] += self.movement[1]
        self.check_bounds()

        ##primitive force decay
        self.movement[0] = self.movement[0] / 1.1
        self.movement[1] = self.movement[1] / 1.1
        if self.movement[1] < 1 and self.movement[1] > -1:
            self.movement[1] = 0

    # check if out of bounds

    def check_bounds(self):
        if self.position[0] < 0 - self.sprite.get_width() or self.position[0] > self.screen.get_width() + 1 or self.position[1] < 0 - self.sprite.get_height() or self.position[1] > self.screen.get_height() + 1:
            self.out_of_bounds = True


# terrain object
class Terrain(Object):
    # overload to avoid needless calculations
    def displace(self):
        self.rect.topleft = (self.position[0], self.position[1])


# Character object, by default Troll npc
class Character(Object):
    grounded = False
    grav = 2
    frame = 0
    turned_left = False
    last_ground = None

    def __init__(self, position, screen):

        super().__init__(position, textures.troll_idle[0], screen)
        characters.append(self)
        self.movement = [0, -10]

    # simple method to check whether character is on the ground based on movement vector
    def check_grounded(self):
        "Obsolete. Use handle_collides()"
        ####                self.handle_collides(terrains)
        ##                if self.movement[1]!=0:
        ##                        self.grounded = False
        ##                else:
        ##                        self.grounded = True
        return 0

    def draw(self):
        super().draw()

    # collision detection with Terrain to manage whether gravity will affect character
    def handle_collides(self, terrain):

        if pygame.sprite.collide_rect(self, terrain):
            ##                                if self.rect.bottom >= terrain.rect.top and self.rect.bottom <= terrain.rect.bottom and (self.rect.midbottom[0]+10 in range(terrain.rect.left, terrain.rect.right) or self.rect.midbottom[0]-10 in range(terrain.rect.left, terrain.rect.right)):

            if type(terrain) is Terrain:
                self.position[1] = terrain.position[1] - self.sprite.get_height()
                # needs to upgrade rect coordinates for jumping to work, since jump is called afterwards
                self.displace()
                if self.last_ground is not terrain:
                    self.decide_move_dir()
                self.grounded = True
                self.last_ground = terrain

    # apply constant falling force unless grounded
    # separated to 3 stages to stop gravity at the exact moment collision is detected
    def gravity(self):
        if not self.grounded:
            self.movement[1] += self.grav
            ##                                if self.movement[1] <-50:
            ##                                        self.movement[1] = -50

    # name self explanatory. sadly pygame doesnt support gifs, hence this (very mediocre) workaround
    def animate(self):
        if self.frame > 30:
            self.frame = -30
        if self.frame % 5 == 0:
            # goes into negative for a simple rotation from 1-6 and then back from 6-1, rather than jumping straight back to 0
            self.sprite = pygame.transform.flip(pygame.Surface.copy(textures.troll_idle[abs(int(self.frame / 5))]),self.turned_left, False)
        self.frame += 1

    ## upon falling on another platform, decide whether to go left or right
    def decide_move_dir(self):
        decision = random.randint(0, 2)
        if decision != 1:
            self.turned_left = False
        else:
            self.turned_left = True

    def update(self):
        self.check_grounded()
        self.gravity()
        self.animate()
        self.displace()
        self.grounded = False
        if self.turned_left:
            self.movement[0] = -1
        else:
            self.movement[0] = 1


# Extending Character class to make a troll into a controllable knight
class Player(Character):
    grav = 2
    attacked = False
    animation_frame = 0

    def __init__(self, position, screen):
        super().__init__(position, screen)
        self.sprite = textures.player_idle
        movement = [0, 10]

    ##update position based on input
    def update(self):
        if self.movement[0]>0:
            self.turned_left = False
        if self.movement[0]<0:
            self.turned_left = True
        if self.attacked:
            self.sprite = pygame.transform.flip(pygame.Surface.copy(textures.player_attack), self.turned_left, False)
        else:
            self.sprite = pygame.transform.flip(pygame.Surface.copy(textures.player_idle), self.turned_left, False)
        self.check_grounded()

        self.gravity()
        self.get_controls()
        self.displace()

        self.grounded = False

    ##get user input to determine action
    def get_controls(self):
        pressed = pygame.key.get_pressed()
        x = 0
        y = 0
        if pressed[pygame.K_UP] and self.grounded == True:
            y -= 15
        # if pressed[pygame.K_DOWN] and self.grounded == False: y += 2##I dont need a dive in this game... Also, it'd be inconvenient for gravity implementation.
        if pressed[pygame.K_LEFT]: x -= 1.5
        if pressed[pygame.K_RIGHT]: x += 1.5

        self.action(pressed[pygame.K_SPACE])

        direction = [x, y]
        self.move(direction)

    def handle_killing(self, npc):
        if pygame.sprite.collide_rect(self, npc) and self.attacked:
            characters.remove(npc)
            objects.remove(npc)
            return True
        else:
            return False

    # character action - limit attack to 8 frames max to avoid button-hold for endless attack
    def action(self, should_act):
        if should_act:
            if self.animation_frame < 15:
                self.animation_frame += 1
            else:
                self.animation_frame = 0
        else:
            self.animation_frame = 0
        if self.animation_frame < 8 and self.animation_frame != 0:
            self.attacked = True
        else:
            self.attacked = False


            ##add movement vector from keyboard inputs

    def move(self, direction):
        self.movement[0] += direction[0]
        self.movement[1] += direction[1]



##player object in map edition mode - same type for same referencing in edition mode
class Editor(Player):
    def __init__(self, position, screen):
        super().__init__(position, screen)
        self.sprite = textures.platform
        self.movement = [0, 0]
        self.save_and_quit = False
        self.quit = False

    # avoid keydown resulting in putting terrain object every frame
    built = False
    # switch between building and erasing mode
    building = True
    changed = False

    ##overload update method to prevent gameplay elements like gravity
    def update(self):
        self.get_controls()
        self.displace()
        if self.building:
            self.sprite = pygame.Surface.copy(textures.platform)

        else:
            self.sprite.fill((128, 0, 0))

    ##overload action for editor mode
    def action(self, should_act):
        if should_act and self.built == False:
            if self.building:
                objects.append(Terrain(self.position[:], textures.platform, self.screen))
                self.built = True
            else:
                for x in objects:
                    self.handle_collides(x)
    # overloading controls
    def get_controls(self):
        pressed = pygame.key.get_pressed()
        x = 0
        y = 0

        if pressed[pygame.K_UP]: y -= 2
        if pressed[pygame.K_DOWN]: y += 2
        if pressed[pygame.K_LEFT]: x -= 2
        if pressed[pygame.K_RIGHT]: x += 2

        if not pressed[pygame.K_SPACE]: self.built = False
        if not pressed[pygame.K_LCTRL]: self.changed = False
        if pressed[pygame.K_ESCAPE]:
            self.quit = True
        if pressed[pygame.K_RETURN]:
            self.save_and_quit = True

        self.action(pressed[pygame.K_SPACE])
        self.mode(pressed[pygame.K_LCTRL])
        direction = [x, y]
        self.move(direction)
        # handle edition and removal mode

    def mode(self, should_change):
        if should_change and not self.changed:
            self.building = not self.building
            self.changed = True
            # collision detection to determine objects to remove

    def handle_collides(self, terrain):
        if pygame.sprite.collide_rect(self, terrain):
            if type(terrain) is Terrain:
                objects.remove(terrain)
