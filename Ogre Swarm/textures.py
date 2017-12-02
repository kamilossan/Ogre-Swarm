import entities
import os
import pygame

_image_library = {}


##Source:http://www.nerdparadise.com/programming/pygame/part2
##load sprite if not yet loaded, otherwise read from library/convert normal file path into system-specific
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


global player_attack
global player_idle
global platform
global troll_idle
troll_idle = []

for x in range(0, 7):
    filename = "RUN_00" + str(x) + ".png"
    img = get_image(filename)
    img = pygame.transform.scale(img, (int(img.get_width() / 8), int(img.get_height() / 8)))
    troll_idle.append(img)
player_attack = get_image("player_attack.png")
# player_attack = pygame.transform.scale(player_attack, (60,120))
player_idle = get_image("player_idle.png")
# player_idle = pygame.transform.scale(player_idle, (60,120))
platform = get_image('platform.png')
platform = pygame.transform.scale(platform, (120, 30))


def background(screen_size):
    bg = get_image('38.png')
    bg = pygame.transform.scale(bg, screen_size)
    return bg
