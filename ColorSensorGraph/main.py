import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wg
import pygame
from pygame.locals import *
import serial
import time
import sys

DEVICE_COM = "COM5"

intensData = [0, 0, 0]
compensateValue = 0.5
########## R is max ##########
redOriginalData = [1000, 240, 210]
redRateMin = [redOriginalData[0], redOriginalData[1]*(1-compensateValue), redOriginalData[2]*(1-compensateValue)]
redRateMax = [redOriginalData[0], redOriginalData[1]*(1+compensateValue), redOriginalData[2]*(1+compensateValue)]
magentaOriginalData = [1000, 228, 301]
magentaRateMin = [magentaOriginalData[0], magentaOriginalData[1]*(1-compensateValue), magentaOriginalData[2]*(1-compensateValue)]
magentaRateMax = [magentaOriginalData[0], magentaOriginalData[1]*(1+compensateValue), magentaOriginalData[2]*(1+compensateValue)]
yellowOriginalData = [1000, 980, 370]
yellowRateMin = [yellowOriginalData[0], yellowOriginalData[1]*(1-compensateValue), yellowOriginalData[2]*(1-compensateValue)]
yellowRateMax = [yellowOriginalData[0], yellowOriginalData[1]*(1+compensateValue), yellowOriginalData[2]*(1+compensateValue)]
########## G is max ##########
greenOriginalData = [547, 1000, 679]
greenRateMin = [greenOriginalData[0]*(1-compensateValue), greenOriginalData[1], greenOriginalData[2]*(1-compensateValue)]
greenRateMax = [greenOriginalData[0]*(1+compensateValue), greenOriginalData[1], greenOriginalData[2]*(1+compensateValue)]
########## B is max ##########
cyanOriginalData = [330, 687, 1000]
cyanRateMin = [cyanOriginalData[0]*(1-compensateValue), cyanOriginalData[1]*(1-compensateValue), cyanOriginalData[2]]
cyanRateMax = [cyanOriginalData[0]*(1+compensateValue), cyanOriginalData[1]*(1+compensateValue), cyanOriginalData[2]]
blueOriginalData = [890, 677, 1000]
blueRateMin = [blueOriginalData[0]*(1-compensateValue), blueOriginalData[1]*(1-compensateValue), blueOriginalData[2]]
blueRateMax = [blueOriginalData[0]*(1+compensateValue), blueOriginalData[1]*(1+compensateValue), blueOriginalData[2]]

def getColor(rd: str, gr: str, bl: str) -> str:
    color = 'BLACK'
    maxColor = 0
    maxColorIntens = 0
    intensData[0] = int(rd)
    intensData[1] = int(gr)
    intensData[2] = int(bl)
    print('intensData: ', intensData)

    for i, intens in enumerate(intensData):
        if intens > maxColorIntens:
            maxColorIntens = intens
            maxColor = i
    normalizedData = list(map(lambda x: int(x * 1000 / maxColorIntens), intensData))
    normalizedData = [intensData[0], intensData[1], intensData[2]]*1000/maxColorIntens
    print('maxColor: ', maxColor)
    print('maxColorIntens: ', maxColorIntens)
    print('normalizedData: ', normalizedData)

    if maxColor == 0:
        # マゼンタかどうか
        if normalizedData[1] > magentaRateMin[1] and normalizedData[1] < magentaRateMax[1] and\
            normalizedData[2] > magentaRateMin[2] and normalizedData[2] < magentaRateMax[2] and\
            normalizedData[1] < normalizedData[2]:
            color = 'MAGENTA'
        # 赤かどうか
        elif normalizedData[1] > redRateMin[1] and normalizedData[1] < redRateMax[1] and\
            normalizedData[2] > redRateMin[2] and normalizedData[2] < redRateMax[2]:
            color = 'RED'
        # 黄かどうか
        elif normalizedData[1] > yellowRateMin[1] and normalizedData[1] < yellowRateMax[1] and\
            normalizedData[2] > yellowRateMin[2] and normalizedData[2] < yellowRateMax[2]:
            color = 'YELLOW'
    elif maxColor == 1:
        # 緑かどうか
        if normalizedData[0] > greenRateMin[0] and normalizedData[0] < greenRateMax[0] and\
            normalizedData[2] > greenRateMin[2] and normalizedData[2] < greenRateMax[2]:
            color = 'GREEN'
    else:
        # シアンかどうか
        if normalizedData[0] > cyanRateMin[0] and normalizedData[0] < cyanRateMax[0] and\
            normalizedData[1] > cyanRateMin[1] and normalizedData[1] < cyanRateMax[1] and\
            normalizedData[0] < normalizedData[1]:
            color = 'CYAN'
        # 青かどうか
        elif normalizedData[0] > blueRateMin[0] and normalizedData[0] < blueRateMax[0] and\
            normalizedData[1] > blueRateMin[1] and normalizedData[1] < blueRateMax[1]:
            color = 'BLUE'

    return color


def main():
    try:
        ser = serial.Serial(DEVICE_COM, 9600, timeout=1)
        print(ser)
    except Exception as e:
        print('[Error]', e)
        exit()

    serialStatus = False
    color = ''
    redValue, greenValue, blueValue = str(0), str(0), str(0)

    redValues = [0]*101
    greenValues = [0]*101
    blueValues = [0]*101
    t = np.arange(0,101,1)

    #  グラフ表示設定
    line1, = plt.plot(t, redValues, 'r-', label="RED")
    line2, = plt.plot(t, greenValues, 'g-', label="GREEN")
    line3, = plt.plot(t, blueValues, 'b-', label="BLUE")
    plt.title("Realtime RGB Sensing")
    plt.xlabel("Time [s]")
    plt.ylabel("Intensitiy []")
    plt.legend(); plt.grid()
    plt.xlim([0,100]); plt.ylim([0,1023])
    plt.ion()
    # axColor = 'lightgoldenrodyellow'
    # axSerial = plt.axes([0.2, 0.1, 0.15, 0.05])
    # btnSerial = wg.Button(axSerial, 'START', color=axColor, hoverColor='#CCFFCC') 

    # Pygameの設定
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("RGBカラーセンサ")
    font = pygame.font.Font(None, 30)

    # redData = 0
    # greenData = 0
    # blueData = 0
    # redIncrementStatus = True
    # greenIncrementStatus = True
    # blueIncrementStatus = False

    while True:
        # pygameの処理
        for event in pygame.event.get():
            # 終了ボタンが押されたら終了
            if event.type == QUIT:
                pygame.quit()
                ser.close()
                plt.close()
                sys.exit()
        mBtn1 = pygame.mouse.get_pressed()[0]

        screen.fill((0,0,0))
        text1 = font.render("(R, G, B) = ("+redValue+", "+greenValue+", "+blueValue+")", False, (255,255,255))
        text2 = font.render("Color is " + color, False, (255,255,255))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 100))
        pygame.display.flip()

        if serialStatus == False:
            if mBtn1:
                serialStatus = True
                ser.write(b'python')
                print('R,  G,  B')

        try:
            serialRx = str(ser.readline().rstrip())

        except Exception as e:
            print('[Error]', e)
            exit()
                
        if 'RGB' in serialRx:
            startNum = serialRx.find('RGB') + 5
            data = serialRx[startNum:-1]

            # data = rgbData.split(',')
            # data = "{},{},{}".format(redData, greenData, blueData)

            # if (redIncrementStatus == True and redData < 1023):
            #     redData += 10
            #     if redData > 1023:
            #         redData = 1023
            # elif redData == 1023:
            #     redIncrementStatus = False
            #     redData -= 10
            # else:
            #     redData -= 10
            #     if redData < 0:
            #         redData = 0
            #     if redData == 0:
            #         redIncrementStatus = True

            # if (greenIncrementStatus == True and greenData < 1023):
            #     greenData += 10
            #     if greenData > 1023:
            #         greenData = 1023
            # elif greenData == 1023:
            #     greenIncrementStatus = False
            #     greenData -= 10
            # else:
            #     greenData -= 10
            #     if greenData < 0:
            #         greenData = 0
            #     if greenData == 0:
            #         greenIncrementStatus = True

            # if (blueIncrementStatus == True and blueData < 1023):
            #     blueData += 10
            #     if blueData > 1023:
            #         blueData = 1023
            # elif blueData == 1023:
            #     blueIncrementStatus = False
            #     blueData -= 10
            # else:
            #     blueData -= 10
            #     if blueData < 0:
            #         blueData = 0
            #     if blueData == 0:
            #         blueIncrementStatus = True
            
            (redValue, greenValue, blueValue) = data.split(",")
            print(redValue + ', ' + greenValue + ', ', blueValue)
            color = getColor(redValue, greenValue, blueValue)
            print('color: ', color)

            redValues.pop(100)
            redValues.insert(0, int(redValue))
            greenValues.pop(100)
            greenValues.insert(0, int(greenValue))
            blueValues.pop(100)
            blueValues.insert(0, int(blueValue))

            line1.set_ydata(redValues)
            line2.set_ydata(greenValues)
            line3.set_ydata(blueValues)
            plt.draw()
            plt.pause(0.05)


if __name__ == '__main__':
    main()
