import matplotlib.pyplot as plt
from PIL import Image
import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import os

def fixText(s):
    return s.replace('\n\n','\n').replace(' ', '').replace('|', 'I')

def processForText(image, removeBorders=True):
    result = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    if removeBorders:
        vShift = 15
        b = result.shape[0] // 12
        newImg = np.zeros((b*4, b*4, 3), dtype=np.uint8)
        for i in range(4):
            for j in range(4):
                newImg[b*i:b*(i+1),b*j:b*(j+1)] = \
                    result[b*(3*i+1)+vShift:b*(3*i+2)+vShift,b*(3*j+1):b*(3*j+2)]
        result = newImg
    result = cv2.inRange(result, (0,0,0), (25,25,25))
    kernel = np.ones((3,3), dtype='uint8')
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel, iterations=3)
    #result = cv2.dilate(result,kernel,iterations=1)
    result = cv2.GaussianBlur(result, (11,11), 0)
    result = 255 - result
    return result

image = None

def getImage(file=None, updateImage=True):
    global image
    if type(image) == type(None) or updateImage or file:
        if not file:
            thisTime = str(int(time.time()))
            pyautogui.screenshot(f'screenshots/{thisTime}_full.png')
            pyautogui.screenshot(f'screenshots/{thisTime}.png', (328,333,290,290))
            image = cv2.imread(f'screenshots/{thisTime}.png')
        else:
            image = cv2.imread(file)
    return image

def getMultMask(c1,c2,file=None,display=False,updateImage=False):
    global image
    start = time.perf_counter()
    getImage(file, updateImage)
    #hlsImage = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    kernel = np.ones((3,3), dtype='uint8')
    result = cv2.inRange(image,c1,c2)
    #plt.imshow(result, cmap='gray'); plt.show()
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel, iterations=30)
    result = cv2.resize(result, None, fx=4/290, fy=4/290, interpolation=cv2.INTER_CUBIC)
    return result

def getMult(file=None,display=False,updateImage=False):
    global image
    start = time.perf_counter()
    getImage(file, updateImage)
    kernel = np.ones((3,3), dtype='uint8')
    L2 = getMultMask((185,165,91),(224,216,176))
    L3 = getMultMask((246,144,194),(255,187,213))
    W2 = getMultMask((107,5,244),(173,137,255))
    W3 = getMultMask((87,195,245),(159,215,255))
    L = (L2//255) + (L3//127) + 1
    W = (W2//255) + (W3//127) + 1
    #plt.imshow(cv2.cvtColor(W3, cv2.COLOR_BGR2RGB))
    #plt.show()
    if display:
        print(time.perf_counter() - start)
        print(L, W, sep='\n')
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.show()
    return L, W

def getText(file=None,display=False,updateImage=True):
    global image
    start = time.perf_counter()
    getImage(file, updateImage)
    result = processForText(image)
    d = pytesseract.image_to_string(result, lang='eng',
            config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHI|JKLMNOPQRSTUVWXYZ')
    if display:
        print(time.perf_counter() - start)
        #print(d)
        #for l, t, w, h, conf in zip(d['left'], d['top'], d['width'], d['height'], d['conf']):
        #    if int(conf) >= 0:
        #        #print(l, t, w, h)
        #        result = cv2.rectangle(result, (l, t), (l+w, t+h), 0, 3)
        print(fixText(d))
        #cv2.imwrite('output.jpg', result)
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        plt.show()
        #cv2.imshow('output.jpg', result)
    return fixText(d)

if __name__ == '__main__':
    #getMult('examples/IEOL.png',display=True)
    for file in os.listdir('examples'):
        if file.endswith('png'):
            print(file)
            getText(f'examples/{file}', True)
            #getMult(display=True)
    #getText('examples/ITVM.png', True)
