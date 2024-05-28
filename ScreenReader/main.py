import time

from ScreenReader.ScreenData import Energy

if "__main__" == __name__:
    time.sleep(1)
    energy = Energy()
    energy.update()
