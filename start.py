import pygame
import sys
import time
import serial
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)
BLACK = (0, 0, 0)
arr = [] #array for player 1
arr1 = [] #array for player 2
temp = [] #array for storing raw data


class Init:
    def __init__(self):
        pygame.init()
        self.FPS = 60
        self.WIN_WIDTH = 1280
        self.WIN_HEIGHT = 720
        self.r = 30
        self.x = self.WIN_WIDTH // 2
        self.y = self.WIN_HEIGHT // 2
        self.myfont = pygame.font.SysFont('comicsansms', 50)
        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        self.start = self.myfont.render("PRESS ENTER TO BEGIN", True, ORANGE)
        self.first = self.myfont.render("FIRST WON. PRESS ENTER TO CONTINUE", True, ORANGE)
        self.second = self.myfont.render("SECOND WON. PRESS ENTER TO CONTINUE", True, ORANGE)
        self.sc = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.text = ""

    def stillArm(self, ser):
        for i in range(24):
            try:
                s = ser.readline()
            except:
                raise ValueError("Enter a valid COM Port")
                exit()
            
            string = s.decode('utf-8', 'ignore').replace("\n","")[:-1]

            if string[0]=="#" and string[-1]=="%":
                temp = list(map(int, string[1:-1].split()))
                if len(temp)==2:
                    arr.append(temp[0])
                    arr1.append(temp[1])
        
        sred = sum(arr)/24
        sred1 = sum(arr1)/24
        return sred, sred1


    def startScreen(self, flag, active):
        self.sc.blit(self.start, (350, self.y))
        pygame.display.update()
        for j in pygame.event.get():
            if j.type == pygame.KEYDOWN:
                if j.key == pygame.K_RETURN:
                    flag=not(flag)
  
            elif j.type == pygame.QUIT:
                exit()
                sys.exit()
  
  
            if j.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(j.pos):
                    active = not active
                else:
                    active = False
                color = self.color_active if active else self.color_inactive


            if j.type == pygame.KEYDOWN:
                if active:
                    if j.key == pygame.K_RETURN:
                        ser = serial.Serial("COM"+self.text, 9600)
                        #gathering data to calc average value of still arm
                        sred, sred1 = self.stillArm(ser)
                        text = ''
  
                    elif j.key == pygame.K_BACKSPACE:
                        text = text[:-1]
  
                    else:
                        text += j.unicode
  
        txt_surface = Init.font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        sc.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(sc, color, self.input_box, 2)

        pygame.display.flip()
        clock.tick(30)

        return ser, flag, active, sred, sred1
        