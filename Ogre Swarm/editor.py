import entities, pygame, os, pickle
from textures import *

map_data = []
# initialize basic pygame data, set screen values
pygame.init()
clock = pygame.time.Clock()
print("clock set")
screen_size = (1024, 768)
screen = pygame.display.set_mode(screen_size)
bg = background(screen_size)
screen.blit(bg, (0, 0))
pygame.display.flip()
font = pygame.font.SysFont("impact", 28, False)
prompt = "CTRL - switch between building/deleting\n SPACE - build/delete"
prompt2= "ESC - quit without saving\n ENTER - save&quit"
msg = font.render(prompt,1, (255,0, 80))
msg2 = font.render(prompt2, 1, (255,0,80))

print("screen preparation complete")

# insert editor controller
x = entities.Editor([0, 0], screen)
print("editor controller set")

# editor loop
while not x.save_and_quit and not x.quit:
    screen.blit(bg, (0, 0))
    screen.blit(msg, (0,0))
    screen.blit(msg2, (0,50))
    for s in entities.objects:

        s.draw()
        s.update()
    x.update()
    x.draw()
    clock.tick(60)
    pygame.display.flip()
    pygame.event.get()
    # close app
if x.save_and_quit==True:

    for obj in entities.objects:
        if type(obj) is entities.Terrain:
            map_data.append(obj.position)

            pickle.dump(map_data, open("maps.dat", "wb"))

pygame.quit()
