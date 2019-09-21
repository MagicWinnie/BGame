import pygame
import sys
import time
import serial
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# try:
#     ser = serial.Serial("COM12", 9600)
# except:
#     print("[ERROR] CHOOSE THE COM PORT")
#     exit()
#colors
WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)
BLACK = (0, 0, 0)
#colors

#pygame init start
FPS = 60
WIN_WIDTH = 1280
WIN_HEIGHT = 720
#stuff related to the circle
r = 30
x = WIN_WIDTH // 2
y = WIN_HEIGHT // 2
#stuff related to the circle
pygame.init()
# pygame text init
myfont = pygame.font.SysFont('comicsansms', 50)
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
start = myfont.render("PRESS ENTER TO BEGIN", True, ORANGE)
first = myfont.render("FIRST WON. PRESS ENTER TO CONTINUE", True, ORANGE)
second = myfont.render("SECOND WON. PRESS ENTER TO CONTINUE", True, ORANGE)
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

input_box = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False
#pygame init done

#vars
arr = [] #array for player 1
arr1 = [] #array for player 2
temp = [] #array for storing raw data
su = 0 #sum for player 1
su1 = 0 #sum for player 2
flag = True
#vars

time.sleep(2.0)


#done
while True:
    if flag:
        x = WIN_WIDTH // 2
        y = WIN_HEIGHT // 2
        
        sc.blit(start, (350, y))
        pygame.display.update()
        for j in pygame.event.get():
            if j.type == pygame.KEYDOWN:
                if j.key == pygame.K_RETURN:
                    flag=not(flag)
            elif j.type == pygame.QUIT:
                exit()
                sys.exit()
            if j.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(j.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if j.type == pygame.KEYDOWN:
                if active:
                    if j.key == pygame.K_RETURN:
                        print(text)
                        ser = serial.Serial("COM"+text, 9600)
                        #gathering data to calc average value of still arm
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
                        print(sred, sred1)
                        text = ''
                    elif j.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += j.unicode
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        sc.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(sc, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
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
        pygame.draw.circle(sc, ORANGE, (x, y), r)
        pygame.display.update()
        if x >= WIN_WIDTH:
            # print("FIRST WON. PRESS ENTER TO EXIT")
            sc.blit(first, (150, y))
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
        if x <= 0:
            # print("SECOND WON. PRESS ENTER TO EXIT")
            sc.blit(second, (110, y))
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
