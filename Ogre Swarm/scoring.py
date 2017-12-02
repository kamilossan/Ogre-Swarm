import pygame


#game instance
class Game():
    #defaults
    def __init__(self):
        pygame.font.init()
        self.clock = 0
        self.score = 0
        self.lives = 5
        self.board = ""
        self.game_over = False
        self.font = pygame.font.SysFont("impact", 15)
        self.font1 = pygame.font.SysFont("impact", 20)
        self.end_font = pygame.font.SysFont("impact", 80)
    #handle scoring on kill
    def enemy_kill(self):
        self.score += 10
        self.board += "Enemy slain!\nScore +10\n"
    #handle scoring on player falling off bounds
    def player_fell(self):
        self.score -= 20
        self.board += "Don't run away!\nScore-20\n"
    #handle scoring on monster reaching out of bounds
    def monster_passed(self):
        self.lives -= 1
        self.board += "Monster slipped!\nLive -1\n"
    #prompt score updates on upper left corner, make prompts remain for 200 frames~3 seconds before flushing board
    def screen_prompt(self, screen):
        if not self.game_over:
            msg = "Score:"
            msg+= str(self.score) + "\n" + self.board
            msg = self.font.render(msg, 1, (128, 10, 50))
            screen.blit(msg, (0, 0))
            life = self.font1.render("Lives: "+str(self.lives), 1, (100, 255, 20))
            screen.blit(life, (0, 50))
            if self.clock<=300:
                self.clock+=1
            else:
                self.board = ""
                self.clock =0
        else:
            msg = "Game Over! Score: "+str(self.score)
            msg = self.end_font.render(msg, 1, (255, 80, 10) )
            msg2 = "Press Enter to exit"
            msg2 = self.font.render(msg2, 1, (255, 30, 20))
            screen.blit(msg,screen.get_rect().midleft)
            screen.blit(msg2, screen.get_rect().topleft )
    #define game over
    def check_gameover(self):
        if self.lives < 1:
            self.game_over = True
