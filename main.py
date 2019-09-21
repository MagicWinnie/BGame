from start import Init
import pygame
import sys
import time
import serial
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

#colors
WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)
BLACK = (0, 0, 0)
#colors

#pygame init start
input_box = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False
Init()
time.sleep(1)
sc = Init.sc
clock = Init.clock
FPS = Init.FPS
#pygame init done


#vars
arr = [] #array for player 1
arr1 = [] #array for player 2
temp = [] #array for storing raw data
su = 0 #sum for player 1
su1 = 0 #sum for player 2
flag = True
#vars
#done
while True:
    if flag:
        ser, falg, active, sred, sred1 = Init.startScreen(flag, active)
    elif not(flag):
        sc.fill(BLACK)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
                sys.exit()
        #reading serial
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
        del arr[0]
        del arr1[0]
        #done
        #filters
        a = signal.medfilt(arr)
        a1 = signal.medfilt(arr1)
        if1 = (max(a)+min(a))/2
        if2 = (max(a1)+min(a1))/2
        if if1 > sred and if2 < if1 and if1-if2 > 12:
            x+=5
            print("X IS GROWING")
        elif if2 > sred1 and if1 < if2 and if2 - if1 > 12:
            x-=5
            print("X IS DESCENDING")
        pygame.draw.circle(sc, ORANGE, (Init.x, Init.y), Init.r)
        pygame.display.update()
        if Init.x >= Init.WIN_WIDTH:
            # print("FIRST WON. PRESS ENTER TO EXIT")
            sc.blit(Init.first, (150, Init.y))
            pygame.display.update()
            for j in pygame.event.get():
                if j.type == pygame.KEYDOWN:
                    if j.key == pygame.K_RETURN:
                        flag=not(flag)
                        sc.fill(BLACK)
                        pygame.display.update()
                elif j.type == pygame.QUIT:
                    exit()
                    sys.exit()
        if Init.x <= 0:
            # print("SECOND WON. PRESS ENTER TO EXIT")
            sc.blit(Init.second, (110, Init.y))
            pygame.display.update()
            for j in pygame.event.get():
                if j.type == pygame.KEYDOWN:
                    if j.key == pygame.K_RETURN:
                        flag=not(flag)
                        sc.fill(BLACK)
                        pygame.display.update()
                elif j.type == pygame.QUIT:
                    exit()
                    sys.exit()
        clock.tick(FPS)