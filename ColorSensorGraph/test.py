import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import serial
import time
import sys

DEVICE_COM = "COM5"

def main():
    # ser = serial.Serial(DEVICE_COM)
    redValues = [0]*100
    greenValues = [0]*100
    blueValues = [0]*100
    t = np.arange(0,100,1)
    plt.ion()

    # Pygameの設定
    pygame.init()
    screen = pygame.display.set_mode((300, 100))
    pygame.display.set_caption("RGBカラーセンサ")
    font = pygame.font.Font(None, 30)

    while True:
        # data = ser.readline().rstrip()
        data = "1,10"
        (redValue
        , blueValue) = data.split(",")
        # (redValue, greenValue, blueValue) = data.split(",")

        redValues.pop(99)
        redValues.insert(0, int(redValue))
        # greenValues.pop(99)
        # greenValues.insert(0, int(greenValue))
        blueValues.pop(99)
        blueValues.insert(0, int(blueValue))

        line, = plt.plot(t, redValues, 'r-', label="RED")
        # line, = plt.plot(t, greenValues, 'g-', label="GREEN")
        line, = plt.plot(t, blueValues, 'b-', label="BLUE")
        line.set_ydata(redValues)
        # line.set_ydata(greenValues)
        line.set_ydata(blueValues)
        plt.title("Realtime RGB Sensing")
        plt.xlabel("Time [s]")
        plt.ylabel("Intensitiy []")
        plt.legend(); plt.grid()
        plt.xlim([1,100]); plt.ylim([0,100])
        plt.draw(); plt.clf()

        # pygameの処理
        screen.fill((0,0,0))
        text = font.render("(R, B) = ("+redValue+", "+blueValue+")", False, (255,255,255))
        # text = font.render("(R, G, B) = ("+redValue+", "+greenValue+", "+blueValue+")", False, (255,255,255))
        screen.blit(text, (10, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            # 終了ボタンが押されたら終了
            if event.type == QUIT:
                pygame.quit()
                # ser.close()
                plt.close()
                sys.exit()

if __name__ == '__main__':
    main()
