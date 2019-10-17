from functions.imChange import imChange
import time
from functions import walkman
import pygame, sys
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFont

class Game:
    def __init__(self):
        self.pygame = pygame
        self.display_height = 50
        self.display_width = 350
        self.gameDisplay = self.pygame.display.set_mode((self.display_width, self.display_height))
        self.pygame.display.set_caption('Break')
        self.pygame.init()
        self.display(resize=False)
    
    def text_objects(self, text, font):
        black = (0,0,0)
        white = (255,255,255)
        red = (255,0,0)
        textSurface = font.render(text, True, white)
        return textSurface, textSurface.get_rect()

    def close(self):
        self.pygame.quit()
    
    def listen(self):
        isBreak = True
        for event in self.pygame.event.get():
                if event.type == QUIT: isBreak = False
                if event.type == KEYDOWN and event.dict['key'] == 50:
                    print('break')
                pygame.event.pump()
        return isBreak

    def display(self, text='Press (x) or wait for timer to end', resize=True):
        if resize:
            self.display_height = 50
            self.display_width = 120
            self.gameDisplay = self.pygame.display.set_mode((self.display_width, self.display_height))
        black = (0,0,0)
        self.gameDisplay.fill(black)
        largeText = self.pygame.font.Font('helvetica',18)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

def clkFormat(num):
    wrd = str(num)
    if len(wrd) < 2:
        return '0{0:s}'.format(wrd)
    else:
        return wrd

def sec2clk(sec):
    hrs = (int) (sec // 3600)
    sec = sec - hrs * 3600
    mins = (int) (sec // 60)
    sec = sec - mins * 60
    hrs = clkFormat(hrs)
    mins = clkFormat(mins)
    sec = clkFormat(sec)
    return '{0:s}:{1:s}:{2:s}'.format(hrs, mins, sec)

def imBreak(rem, tot, progress):
    W_bg, H_bg = (350, 450)
    background = Image.new('RGB', (W_bg, H_bg), color = (0, 0, 0))
    pointsize = 80
    draw = ImageDraw.Draw(background)
    file = 'images/break/0.png'
    img = Image.open('{0:s}'.format(file), 'r')
    W, H = img.size
    bar_full_w = int(rem * W / tot)
    bar_empty_w = W_bg
    bar_h = H // 15
    base_h = H - bar_h
    # base_w = 

    p = rem / tot

    R = int((1 - p ** 0.7) * 255)
    G = int(p ** 0.7 * 255)
    B = 0

    bar_full = Image.new('RGB', (bar_full_w, bar_h), color=(R, G, B))
    bar_empty = Image.new('RGB', (bar_empty_w, bar_h), color=(R // 4, G // 4, B // 4))
    img.paste(bar_empty, (W_bg // 2 - bar_empty_w // 2, base_h))
    img.paste(bar_full, (W_bg // 2 - bar_empty_w // 2 , base_h))

    bar_w, bar_h = (W_bg // 20 - 6, H_bg // 40)
    bar_full = Image.new('RGB', (bar_w, bar_h), color=(0, 255, 0))
    bar_empty = Image.new('RGB', (bar_w, bar_h), color=(0, 255 // 4, 0))

    full_num = int(progress * 20)
    base_w = 3
    base_h = 0
    cnt = 0
    while cnt < 20:
        if full_num > 0:
            background.paste(bar_full, ((6 + bar_w) * cnt + base_w, base_h))
            full_num -= 1
        else:
            background.paste(bar_empty, ((6 + bar_w) * cnt + base_w, base_h))
        cnt += 1

    font_progress = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf', pointsize * 2 // 5)
    text_progress = '> {0:d}% Complete <'.format(int(progress * 100))
    text_size_progress = draw.textsize(text_progress, font=font_progress) # the size of the text box!
    x_progress = (W_bg / 2) - (text_size_progress[0] / 2)
    y_progress = bar_h + 30 - (text_size_progress[1] / 2)
    draw.text((x_progress, y_progress), text_progress, font=font_progress, fill=(100, 100, 100))

    background.paste(img, (W_bg // 2 - img.size[1] // 2, 80))

    background.save('images/break.png')
    imChange('break', resize=False)

def takeBreak(sec, progress):
    game = Game()
    t = time.time()
    prev = t
    index = 1
    isBreak = True
    while time.time() - t < sec and isBreak:
        timeNow = sec2clk((int)(t + sec - time.time()))
        game.display(timeNow)
        isBreak = game.listen()
        imBreak(t + sec - time.time(), sec, progress)
        time.sleep(1)
    game.close()
    imBreak(0, 1, progress)
    walkman.play('playback/beep.wav')

# def takeBreak(sec):
#     game = Game()
#     t = time.time()
#     prev = t
#     index = 1
#     isBreak = True
#     while index <=5:
#         imChange('break/{0:d}'.format(6 - index))
#         while time.time() - t < index * sec / 5 and isBreak:
#             if time.time() - prev > 1:
#                 # print(sec2clk((int)(t + sec - time.time())), end='\r')
#                 timeNow = sec2clk((int)(t + sec - time.time()))
#                 game.display(timeNow)
#                 prev = time.time()
#             isBreak = game.listen()
#         index = index + 1
#     game.close()
#     imChange('break/0')
#     walkman.play('playback/beep.wav')