import entities
from textures import *
import pygame
import pickle
import scoring
import random


def spawner():
    mob_spawner = []
    for x in range(0, 3):
        # random number from field equal to framerate, hence there should be 3 mobs spawning each second on average
        roll = random.randint(0, 120)
        if roll == 1:
            mob_spawner.append(True)
        else:
            mob_spawner.append(False)
    return mob_spawner


game = scoring.Game()
map_data = pickle.load(open("maps.dat", "rb"))
pygame.init()
clock = pygame.time.Clock()
screen_size = (1024, 768)
bg = background(screen_size)

screen = pygame.display.set_mode(screen_size)
screen.blit(bg, (0, 0))
pygame.display.flip()

bg = bg.convert(screen)

player = entities.Player([0, 0], screen)

troll = entities.Character([500, 20], screen)
platforms = ()
print("generating terrain at:")
for item in map_data:
    print(str(item))
    platforms += (entities.Terrain(item, platform, screen),)

ground = screen_size[0]
while ground>0-platform.get_width():
      platforms+= (entities.Terrain([ground, screen_size[1]-platform.get_height()], platform, screen),)
      ground-=platform.get_width()

for s in platforms:
    s.draw()
while not game.game_over:

    for mob in spawner():
        if mob == True:
            troll = entities.Character([random.randint(100, screen_size[0] - 100), 50], screen)
    screen.blit(bg, (0, 0))

    pygame.event.get()

    for s in platforms:
        s.draw()
        s.update()
        for mobs in entities.characters:
            mobs.handle_collides(s)
    for trolls in entities.characters:
        if type(trolls) is not entities.Player:
            trolls.update()
            trolls.draw()
            if trolls.out_of_bounds:
                entities.characters.remove(trolls)
                game.monster_passed()
            x = player.handle_killing(trolls)
            if x:
                game.enemy_kill()
        elif trolls.out_of_bounds:
            trolls.position = [50, 50]
            trolls.out_of_bounds = False
            trolls.movement[1] = 2
            game.player_fell()

    player.update()
    player.draw()
    game.screen_prompt(screen)
    clock.tick(75)
    pygame.display.flip()
    game.check_gameover()
    pressed = pygame.key.get_pressed()
while not pressed[pygame.K_RETURN]:
    pygame.event.get()
    screen.blit(bg, (0,0))
    pressed  = pygame.key.get_pressed()
    game.screen_prompt(screen)
    pygame.display.flip()
    clock.tick(24)


pygame.quit()