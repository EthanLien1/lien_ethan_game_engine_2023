# This files was created by: Ethan Lien
# content from kids can code: http://kidscancode.org/blog/

# GameDesign
# Goals: player keeps on jumping till he dies
# Rules: player can't fall to the ground or hit mobs
# Feedback: amount of lives left at the top of the screen
# Freedom: player can jump on any platforms

# Future Goals: 
# Jumps on platforms
# 3 lives 
# bell runs faster every 5 seconds

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')




class Game:
   
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
        self.start = False
         
    def new(self):
        # create a group for all sprites
        self.score = 5
        self.lives = 5
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.one_ground = pg.sprite.Group()
        self.dead = False
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST[1:]:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        plat = Platform(*PLATFORM_LIST[0])
        self.all_sprites.add(plat)
        self.one_ground.add(plat)
        self.all_platforms.add(plat)


        # defines the amount of mobs on screen
        for m in range(0,10):
            m = Mob(randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        self.run()

  
    # shows whether the game is running
    def run(self):
        self.playing = True

        # start screen
        while not self.start:
            self.clock.tick(FPS)
            self.events()
            self.show_start_screen()

        # end screen
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            # checks to see if dead
            if not self.dead:
                self.update()
                self.draw()
            elif self.dead:
                self.show_end_screen()

    # creates new platforms randomly on screen
    def new_platform(self):
        # instantiation of the Platform class
        plat = Platform(randint(0, WIDTH-50), randint(20, HEIGHT-40), 90, 20, "moving")
        self.all_sprites.add(plat)
        self.all_platforms.add(plat)
        
    # updates self
    def update(self):
        self.all_sprites.update()

        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5
        # checks to see if the amount of lives is less than 0
        if self.score <= 0:
            self.dead = True
            return
        
         # this prevents the player from jumping up through a platform
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            mhits = pg.sprite.spritecollide(self.player, self.all_mobs, True)
            if hits:
                self.score -= 1
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                    self.player.acc.y = 5
                    self.player.vel.y = 0
            # subtracts score by one if hit mob
            if mhits:
                self.score -= 1
        # if player hits ground, he dies
        ghit = pg.sprite.spritecollide(self.player, self.one_ground, False)
        if ghit:
            self.score -= 3
            

    # checks whether game is running
    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                self.start = True
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Lives: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    # defines characteristics of the text on screen
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    # shows start screen
    def show_start_screen(self):
        self.screen.fill(LIGHT_BLUE)
        # displays instructions
        self.draw_text("INSTRUCTIONS:", FONT, BROWN, WIDTH/2, HEIGHT/2-100-SPACING)
        self.draw_text("Do not fall to the ground or you will DIE!", FONT, BROWN, WIDTH/2, HEIGHT/2-100)
        self.draw_text("If you hit a mob, you will lose a life!", FONT, BROWN, WIDTH/2, HEIGHT/2-100+SPACING)
        self.draw_text("If you hit your head on a platform you will lose a life!", FONT, BROWN, WIDTH/2, HEIGHT/2-100+2*SPACING)
        self.draw_text("You will see the amount of lives left on the top of the screen", FONT, BROWN, WIDTH/2, HEIGHT/2-100+3*SPACING)
        self.draw_text("Press -enter- to start", FONT, BROWN, WIDTH/2, HEIGHT/2-100+7*SPACING)
        # start game if enter is pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            self.start = True
        pg.display.flip()
    # shows the end screen
    def show_end_screen(self):
        self.draw_text("Better luck next time", 22, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()

g = Game()
while g.running:
    g.new()


pg.quit()
