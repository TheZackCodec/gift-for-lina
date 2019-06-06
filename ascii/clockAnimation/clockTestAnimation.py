import time
import os

currentHour = 1
currentMinute = 0
clockFileName = ""

while True:
    for x in range(12):
        for y in range(12):
            #print("Current Hour: " + str(currentHour))
            #print("Current Minute: " + str(currentMinute))

            if currentMinute == 0 or currentMinute == 5:
                clockFileName = "clock" + str(currentHour) + "0" + str(currentMinute) + ".txt"
            else:
                clockFileName = "clock" + str(currentHour) + str(currentMinute) + ".txt"

            file = open(clockFileName, "r")
            print (file.read())

            currentMinute = (currentMinute + 5) % 60
            time.sleep(.1)
            os.system("cls")

        currentHour = (currentHour + 1) % 12
        if currentHour == 0:
            currentHour = 12
