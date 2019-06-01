import time
import os

currentClock = 5
clockFileName = ""

while True:
    for x in range(12):
        clockFileName = "clock" + str(currentClock) + ".txt"
        file = open(clockFileName, "r")
        print (file.read())
        currentClock = (currentClock + 1) % 12
        if currentClock == 0:
            currentClock = 12
        time.sleep(.1)
        os.system("cls")
