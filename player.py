import pyautogui

pyautogui.PAUSE = 0.04

x = 328
y = 333
w = h = 290

def screenPos(y1, x1):
    return x + w*(1 + 2 * x1)/8,\
            y + h*(1 + 2 * y1)/8

def moveTo(y1, x1, duration=0):
    pyautogui.moveTo(*screenPos(y1, x1), duration=duration)

def subTuple(t1, t2):
    return tuple(map(lambda x, y: x - y, t1, t2))

def dragChain(chain):
    moveTo(*chain[0])
    pyautogui.mouseDown()
    direction = (0,0)
    lastPos = chain[0]
    for pos in chain[1:]:
        newDir = subTuple(pos, lastPos)
        if newDir != direction:
            if direction != (0,0):
                moveTo(*lastPos)
            direction = newDir
        lastPos = pos
    moveTo(*chain[-1])
    pyautogui.mouseUp()
