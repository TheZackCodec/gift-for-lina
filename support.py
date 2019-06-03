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

class support():
    heart = open('ascii/heart.txt', 'r').read()
    birthday = open('ascii/birthday.txt', 'r').read()

    """ Suporting Functions object"""
    def __init__(self, maxY, maxX):
        self.starArray = []
        self.maxY = maxY
        self.maxX = maxX
        random.seed(time.time())

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

    def playMusic(self):
        playsound('audio/Daulton Hopkins - Maroon.mp3')

    def heartBeats(self, stdscr):
        epoch = time.time() + 15.6
        pos = self.maxX
        centerY = int(self.maxY / 2)
        while(time.time() < epoch):
            for x in range(self.maxX - 1, 0, -1):
                if(x != pos):
                    stdscr.addch(centerY, x, '-')
            stdscr.refresh()
            time.sleep(.05)
            pos = pos - 1
            tte = round(epoch - time.time(), 1)
            if(tte == 2.9 or tte == 1.0):
                for y in range(0, 6, 1):
                    stdscr.addch(centerY - y, pos, '-')
                    stdscr.addch(centerY + y, pos - 12, '-')
                    stdscr.delch(centerY, pos)
                    pos = pos - 1
                for y in range(6, 0, -1):
                    stdscr.addch(centerY - y, pos, '-')
                    stdscr.addch(centerY + y, pos - 12, '-')
                    stdscr.delch(centerY, pos)
                    pos = pos - 1
                pos = pos + 6

            stdscr.delch(centerY, pos)
        stdscr.erase()


    def scene1(self, stdscr):
        heartWin = curses.newwin(38, 83, int((self.maxY / 2) - (38 / 2) + 4), int((self.maxX / 2) - (83 / 2)))
        birthdayWin = curses.newwin(7, 129, 0, int((self.maxX / 2) - (129/2)))

        self.drawStars(stdscr)
        epoch = time.time() + 29.6
        while(time.time() < epoch):
            self.drawHeart(heartWin)
            self.drawHappyBirthday(birthdayWin)
            stdscr.refresh()
            birthdayWin.refresh()
            heartWin.refresh()
            self.twinkleRandomStar(stdscr)
            time.sleep(.15)
            birthdayWin.erase()
            heartWin.erase()

    def slideShow1(self, photoArr):
        for x in range(0,7):
            photoArr[x].show()
            time.sleep(3.7)

        os.system('pkill display')
