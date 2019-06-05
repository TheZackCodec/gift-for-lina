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

        self.sys = system()

        if(self.isCompatible()):
            self.imageViewer = 'Preview'
        else:
            self.imageViewer = 'display'

        logging.warn("Detected \"%s\" image viewer" % self.imageViewer)
        # for hour in range(1, 12):
        #     for minute in range(0, 55, 5):
        #         logging.debug('Hour: %s\tMinute: %s' % (hour, minute))
        #         if(minute % 2 == 0 and hour < 10):
        #             self.clock.append(open('ascii/clockAnimation/clock%s0%s.txt' % (hour, minute)).read())
        #         elif(minute % 2 == 0 and hour > 10):
        #             self.clock.append(open('ascii/clockAnimation/clock%s%s.txt' % (hour, minute)).read())
        #         else:
        #             self.clock.append(open('ascii/clockAnimation/clock%s%s.txt' % (hour, minute)).read())

        logging.debug("Loaded %s Clock Files" % len(self.clock))

    def __killImageWindows(self):
        os.system('pkill %s' % self.imageViewer)

    def isCompatible(self):
        return self.sys == 'Windows' or self.sys == 'Darwin'

    def drawHappyBirthday(self, stdscr):
        stdscr.addstr(self.birthday)

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

    def drawHeart(self, stdscr):
        stdscr.addstr(self.heart)

    def drawLove(self, stdscr):
        stdscr.addstr(self.love)

    def drawClock(self, stdscr):
        for x in range(0, len(self.clock)):
            stdscr.addstr(self.clock[x])
            stdscr.refresh()
            time.sleep(.175)
            stdscr.erase()

    def playMusic(self):
        sys = system()
        if(self.isCompatible()):
            logging.warn("%s system detected...switching to asynchronous audio operation" % sys)
            playsound('audio/maroon.mp3', False)
        else:
            logging.warn("*nix system detected...falling back to audio child process")
            playsound('audio/maroon.mp3')

    def heartBeats(self, stdscr):
        epoch = time.time() + 15.6
        beat1 = time.time() + 12.7
        beat2 = time.time() + 14.7
        pos = self.maxX - 1
        centerY = int(self.maxY / 2)
        while(time.time() < epoch):
            stdscr.addch(centerY, pos, '-')
            stdscr.refresh()
            time.sleep(15.6 / (self.maxX / 2))
            pos = pos - 1
            tte = round(epoch - time.time(), 1)
            if(tte <= 2.9 or tte <= .9):
                for y in range(0, 6, 1):
                    stdscr.addch(centerY - y, pos, '-')
                    stdscr.addch(centerY + y, pos - 12, '-')
                    pos = pos - 1
                for y in range(6, 0, -1):
                    stdscr.addch(centerY - y, pos, '-')
                    stdscr.addch(centerY + y, pos - 12, '-')
                    pos = pos - 1
                pos = pos - 12
                if(tte <= 2.9):
                    beat1 = None
                elif(tte <= .9):
                    beat2 = None
        stdscr.erase()


    def scene1(self, stdscr):
        stdscr.erase()
        heartWin = curses.newwin(38, 83, int((self.maxY / 2) - (38 / 2) + 4), int((self.maxX / 2) - (83 / 2)))

        self.drawStars(stdscr)
        epoch = time.time() + 7.6
        while(time.time() < epoch):
            self.drawHeart(heartWin)
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
            self.drawHappyBirthday(birthdayWin)
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
            self.drawLove(loveWin)
            stdscr.refresh()
            loveWin.refresh()
            self.twinkleRandomStar(stdscr)
            time.sleep(.15)
            loveWin.erase()

    def scene4(self, stdscr):
        clockWin = curses.newwin(14, 23, self.maxY - 14, self.maxX- 23)

        epoch = time.time() + 14.2
        while(time.time() < epoch):
            self.drawClock(clockWin)

    def slideShow1(self, photoArr):
        for x in range(0,7):
            photoArr[x].show()
            time.sleep(3.7)

        self.__killImageWindows()

    def slideShow2(self, photoArr):
        for x in range(0,7):
            photoArr[x].show()
            time.sleep(3.7)

        self.__killImageWindows()
