import reader
import solver
import player
import time
import re

print('start')
while True:
    s = reader.getText()
    if re.fullmatch(r'(?:\b\w{4}\b\s?){4}', s):
        time.sleep(0.5)
        s = reader.getText()
        print(s)
        start = time.perf_counter()
        L, W = reader.getMult()
        print(L, W, sep='\n')
        solver.lMult = L
        solver.wMult = W
        solver.game = s.split('\n')
        solver.tryEveryTile()
        cm = solver.canMake # for debugging convenience
        sortedCanMake = solver.sortCanMake()
        count = solver.count
        iterWords = iter(sortedCanMake)
        i = 0
        while time.perf_counter() - start < 80: # 1:22.78 timed
            try:
                player.dragChain(solver.canMake[next(iterWords)][1])
                i += 1
            except StopIteration:
                print(f"finished! {72.78 - time.perf_counter() + start} seconds to spare!")
                break
        if i != count:
            print(f'only finished {i} out of {count} words :(')
        break

def listWords():
    print(*sorted(cm, key=lambda x: (len(x), cm[x][0]), reverse=True),sep='\n')

def points():
    return sum(cm[x][0] for x in cm)
