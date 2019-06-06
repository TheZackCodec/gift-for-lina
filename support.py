##############################################
#   Author: Derick Vigne
#   Purpose: Supprting class for screen manipulation,
#   sound, and photos
#
##############################################


import random
import time
import curses
import logging
import os
from playsound import playsound
from platform import system
from threading import Thread


class support():
    heart = open('ascii/heart.txt', 'r').read()
    birthday = open('ascii/birthday.txt', 'r').read()
    love = open('ascii/love.txt', 'r').read()
    clock = []

    """ Suporting Functions object"""
    def __init__(self, maxY, maxX):
        self.starArray = []
        self.maxY = maxY
        self.maxX = maxX

        random.seed(time.time())

        if(self.isCompatible()):
            self.imageViewer = "Preview"
        else:
            self.imageViewer = "display"
        logging.debug("Detected \"%s\" image viewer" % self.imageViewer)

        # for dirpath, dirnames, files in os.walk('ascii/clockAnimation'):
        #     files.sort()
        #     logging.debug(files)
        #     for file in files:
        #         self.clock.append(open("%s/%s" % (dirpath, file)).read())
        currentHour = 1
        currentMinute = 0
        for x in range(12):
            for y in range(12):

                if currentMinute == 0 or currentMinute == 5:
                    clockFileName = "ascii/clockAnimation/clock" + str(currentHour) + "0" + str(currentMinute) + ".txt"
                else:
                    clockFileName = "ascii/clockAnimation/clock" + str(currentHour) + str(currentMinute) + ".txt"

                self.clock.append(open(clockFileName, "r").read())

                currentMinute = (currentMinute + 5) % 60

            currentHour = (currentHour + 1) % 12
            if currentHour == 0:
                currentHour = 12

        logging.debug("Loaded %s Clock Files" % len(self.clock))

    def draw(self, stdscr, str):
        stdscr.addstr(str)

    def drawStars(self, stdscr):
        for ittr in range(0, 100):
            randomY = random.randrange(self.maxY)
            randomX = random.randrange(self.maxX)
            self.starArray.append([randomY, randomX])
            stdscr.addch(randomY, randomX, curses.ACS_DIAMOND, curses.A_DIM)
        logging.debug("Star Array: %s", self.starArray)

    def twinkleRandomStar(self, stdscr):
        for x in range(0, int(len(self.starArray) / 2)):
            randCoordinates = self.starArray[random.randrange(len(self.starArray))]
            if(random.random() > .5):
                stdscr.addch(randCoordinates[0], randCoordinates[1], curses.ACS_DIAMOND, curses.A_BOLD)
            else:
                stdscr.addch(randCoordinates[0], randCoordinates[1], curses.ACS_DIAMOND, curses.A_DIM)

    def drawClock(self, stdscr):
        for x in range(0, len(self.clock)):
            stdscr.addstr(self.clock[x])
            stdscr.refresh()
            time.sleep(.175)
            stdscr.erase()

    def isCompatible(self):
        return system() == "Darwin"

    def playMusic(self):
        if(self.isCompatible()):
            logging.warn("$s system detected...switching to asynchronous audio operation" % system())
            playsound('audio/maroon.mp3', False)
        else:
            logging.warn("*nix system detected...falling back to audio child process")
            playsound('audio/maroon.mp3')


    def heartBeats(self, stdscr):
        epoch = time.time() + 15.6
        pos = self.maxX - 1
        centerY = int(self.maxY / 2)
        while(time.time() < epoch):
            tte = round(epoch - time.time(), 1)
            stdscr.addch(centerY, pos, '-')
            stdscr.refresh()
            time.sleep(15.6 / (self.maxX / 2))
            pos = pos - 1
            if(tte == 2.9 or tte == .9):
                for y in range(0, 6, 1):
                    stdscr.addch(centerY - y, pos, '-')
                    stdscr.addch(centerY + y, pos - 12, '-')
                    pos = pos - 1
                for y in range(6, 0, -1):
                    stdscr.addch(centerY - y, pos, '-')
                    stdscr.addch(centerY + y, pos - 12, '-')
                    pos = pos - 1
                pos = pos - 12
        stdscr.erase()


    def scene1(self, stdscr):
        stdscr.erase()
        heartWin = curses.newwin(38, 83, int((self.maxY / 2) - (38 / 2) + 4), int((self.maxX / 2) - (83 / 2)))

        self.drawStars(stdscr)
        epoch = time.time() + 7.6
        while(time.time() < epoch):
            self.draw(heartWin, self.heart)
            stdscr.refresh()
            heartWin.refresh()
            self.twinkleRandomStar(stdscr)
            time.sleep(.15)
            heartWin.erase()
        heartWin.erase()
        heartWin.refresh()

    def scene2(self, stdscr):
        birthdayWin = curses.newwin(7, 129, int((self.maxY / 2) - (7 / 2) + 2), int((self.maxX / 2) - (129/2)))

        epoch = time.time() + 7.6
        while(time.time() < epoch):
            self.draw(birthdayWin, self.birthday)
            stdscr.refresh()
            birthdayWin.refresh()
            self.twinkleRandomStar(stdscr)
            time.sleep(.15)
            birthdayWin.erase()
        birthdayWin.erase()
        birthdayWin.refresh()

    def scene3(self, stdscr):
        loveWin = curses.newwin(7, 63, int((self.maxY / 2) - (7 / 2) + 2), int((self.maxX / 2) - (63/2)))

        epoch = time.time() + 14.2
        while(time.time() < epoch):
            self.draw(loveWin, self.love)
            stdscr.refresh()
            loveWin.refresh()
            self.twinkleRandomStar(stdscr)
            time.sleep(.15)
            loveWin.erase()

    def _animateClock(self, stdscr):
        for clockTime in self.clock:
            self.draw(stdscr, clockTime)
            stdscr.refresh()
            time.sleep(.25)
            stdscr.erase()

    def scene4(self, stdscr):
        clockWin = curses.newwin(14, 23, self.maxY - 14, self.maxX- 23)

        epoch = time.time() + 14.2
        clock = Thread(name="Clock", target=self._animateClock, args=[clockWin])
        clock.start()

    def _killImageViewer(self):
        os.system('pkill %s' % self.imageViewer)

    def slideShow1(self, photoArr):
        for x in range(0,7):
            photoArr[x].show()
            time.sleep(3.7)

        _killImageViewer()

    def slideShow2(self, photoArr):
        for x in range(0,7):
            photoArr[x].show()
            time.sleep(3.7)

        _killImageViewer()
