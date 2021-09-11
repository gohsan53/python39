# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import serial
import sys
import time

def main():
    ser = serial.Serial("COM7")  # COMポート(Arduino接続)
    xdegs = [0]*101              # 温度格納
    ydegs = [0]*101              # 温度格納
    t = np.arange(0,101,1)

    # グラフ表示設定
    line1, = plt.plot(t, xdegs, 'r-',label="X-axis[deg]") # Y軸更新
    line2, = plt.plot(t, ydegs, 'b-',label="Y-axis[deg]") # Y軸更新
    plt.title("Real-time inclination angle")
    plt.xlabel("Time [s]")
    plt.ylabel("Inclination angle [deg]")
    plt.legend()
    plt.grid()
    plt.xlim([0,100])
    plt.ylim([-90,90])
    plt.ion()
    # Pygameの設定
    pygame.init()                                  # 初期化
    screen = pygame.display.set_mode((200, 200))   # 画面作成(100×100)
    pygame.display.set_caption("傾斜角度")         # タイトルバー
    font = pygame.font.Font(None, 30)              # 文字の設定

    while True:

        # time.sleep(1)
        # data = ser.readline().rstrip()  # \nまで読み込む(\nは削除)
        data = "1,10"
        (xdeg, ydeg) = ('1.1', '10.2')

        # 角度データのリスト更新
        xdegs.pop(100)
        xdegs.insert(0,float(xdeg))
        ydegs.pop(100)
        ydegs.insert(0,float(ydeg))


        line1.set_ydata(xdegs)
        line2.set_ydata(ydegs)
        plt.draw()
        plt.pause(0.05)

        # Pygameの処理
        screen.fill((0,0,0))            # 画面のクリア
        text = font.render("(X, Y) = ("+xdeg+", "+ydeg+")", False, (255,255,255))
        screen.blit(text, (10, 10))     # レンダ，表示位置
        pygame.display.flip()           # 画面を更新して、変更を反映

        # Pygameのイベント処理
        for event in pygame.event.get():
            # 終了ボタンが押されたら終了処理
            if event.type == QUIT:
                pygame.quit()
                # ser.close()
                plt.close()
                sys.exit()


if __name__ == '__main__':
    main()