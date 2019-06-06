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
    car = open('ascii/car.txt', 'r').read()
    rightBubble = open('ascii/bubbleRight.txt', 'r').read()
    leftBubble = open('ascii/bubbleLeft.txt', 'r').read()
    rightHeart = open('ascii/bubbleRightHeart.txt', 'r').read()
    leftHeart = open('ascii/bubbleLeftHeart.txt', 'r').read()
    outro = open('ascii/outro.txt', 'r').read()

    clock = []

    """ Suporting Functions object"""
    def __init__(self, maxY, maxX):
        self.starArray = []
        self.maxY = maxY
        self.maxX = maxX
        self.centerY = int(self.maxY / 2)

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

    def blankScreen(self, stdscr, sleep):
        logging.debug("Supressing output for %s seconds", sleep)
        stdscr.erase()
        epoch = time.time() + sleep
        while(time.time() < epoch):
            stdscr.refresh()

    def drawStars(self, stdscr, numStars):
        self.starArray = []
        for ittr in range(0, numStars):
            randomY = random.randrange(stdscr.getmaxyx()[0])
            randomX = random.randrange(stdscr.getmaxyx()[1])
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

        while(time.time() < epoch):
            tte = round(epoch - time.time(), 1)
            stdscr.addch(self.centerY, pos, '-')
            stdscr.refresh()
            time.sleep(15.6 / (self.maxX / 2))
            pos = pos - 1
            if(tte == 2.9 or tte == .9):
                for y in range(0, 6, 1):
                    stdscr.addch(self.centerY - y, pos, '-')
                    stdscr.addch(self.centerY + y, pos - 12, '-')
                    pos = pos - 1
                for y in range(6, 0, -1):
                    stdscr.addch(self.centerY - y, pos, '-')
                    stdscr.addch(self.centerY + y, pos - 12, '-')
                    pos = pos - 1
                pos = pos - 12
        stdscr.erase()


    def scene1(self, stdscr):
        logging.debug("Scene 1 started")
        stdscr.erase()
        heartWin = curses.newwin(38, 83, int((self.maxY / 2) - (38 / 2) + 4), int((self.maxX / 2) - (83 / 2)))

        self.drawStars(stdscr, 100)
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
        logging.debug("Scene 2 started")
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
        logging.debug("Scene 3 started")
        loveWin = curses.newwin(7, 63, int((self.maxY / 2) - (7 / 2) + 2), int((self.maxX / 2) - (63/2)))

        epoch = time.time() + 14.2
        while(time.time() < epoch):
            self.draw(loveWin, self.love)
            stdscr.refresh()
            loveWin.refresh()
            self.twinkleRandomStar(stdscr)
            time.sleep(.15)
            loveWin.erase()
        loveWin.erase()
        loveWin.refresh()
        stdscr.erase()
        stdscr.refresh()

    def scene4(self, stdscr):
        logging.debug("Scene 4 started")
        starWin = curses.newwin(int(self.maxY * .5), self.maxX -1)
        carWin = curses.newwin(16, 41, int((self.maxY / 2) - (16/2) + 10), int((self.maxX / 2) - (41 / 2)))
        clockWin = curses.newwin(14, 23, self.maxY - 14, self.maxX - 23)
        bubbleWinRight = curses.newwin(15, 25, int((self.maxY / 2) - 10), int((self.maxX / 2) - 42))
        bubbleWinLeft = curses.newwin(15, 25, int((self.maxY / 2) - 10), int((self.maxX / 2) + 16))

        self.draw(bubbleWinRight, self.rightBubble)

        stdscr.refresh()

        epoch = time.time() + 30.6
        clockBeat = time.time() + 15.3
        leftBubbleBeat = time.time() + 7.6

        self.drawStars(starWin, 50)
        self.draw(carWin, self.car)
        self.draw(clockWin, self.clock[0])
        clockIttr = 1
        while(time.time() < epoch):
            starWin.refresh()
            carWin.refresh()
            clockWin.refresh()
            self.twinkleRandomStar(starWin)
            bubbleWinRight.erase()
            self.draw(bubbleWinRight, self.rightBubble)
            bubbleWinRight.addstr(int(bubbleWinRight.getmaxyx()[0] / 2 - 3), int(bubbleWinRight.getmaxyx()[1] / 2 - 3), "...")
            bubbleWinRight.refresh()
            if(time.time() > leftBubbleBeat):
                bubbleWinLeft.erase()
                self.draw(bubbleWinLeft, self.leftBubble)
                bubbleWinLeft.addstr(int(bubbleWinLeft.getmaxyx()[0] / 2 - 3), int(bubbleWinLeft.getmaxyx()[1] / 2 - 3), "...")
                bubbleWinLeft.refresh()
            if(time.time() > clockBeat):
                clockWin.erase()
                bubbleWinRight.erase()
                bubbleWinLeft.erase()
                self.draw(clockWin, self.clock[clockIttr])
                self.draw(bubbleWinLeft, self.leftHeart)
                bubbleWinLeft.refresh()
                self.draw(bubbleWinRight, self.rightHeart)
                bubbleWinRight.refresh()
                clockIttr = clockIttr + 1
            time.sleep(.15)

    def scene5(self, stdscr):
        logging.debug("Scene 5 started")
        stdscr.erase()
        outroWin = curses.newwin(31, 138, int((self.maxY / 2) - (31 / 2) + 4), int((self.maxX / 2) - (138 / 2)))

        self.drawStars(stdscr, 100)
        epoch = time.time() + 34.35
        while(time.time() < epoch):
            self.draw(outroWin, self.outro)
            stdscr.refresh()
            outroWin.refresh()
            self.twinkleRandomStar(stdscr)
            time.sleep(.15)
            outroWin.erase()
        outroWin.erase()
        outroWin.refresh()


    def _killImageViewer(self):
        logging.debug("Killing %s processes", self.imageViewer)
        os.system('pkill %s' % self.imageViewer)

    def playSlideShow(self, photoArr, start, end):
        logging.debug("Opening photos %s through %s" % (start + 1, end + 1))
        for x in range(start, end):
            photoArr[x].show()
            time.sleep(3.7)
            if((x + 1) % 4 == 0):
                self._killImageViewer()

        self._killImageViewer()
