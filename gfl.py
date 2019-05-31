##############################################
#   Author: Derick Vigne
#   Todo:
#   - Replace MaxY, MaxX with functional arguments
#   - Organize into story pages or phases
#
##############################################

import os, sys
import logging
import random
import time
import curses

heart = open('ascii/heart.txt', 'r').read()
birthday = open('ascii/birthday.txt', 'r').read()

starArray = []

def drawHappyBirthday(stdscr, maxY, maxX):
    logging.debug("Max Y, X: %s, %s" % (maxY, maxX))
    stdscr.addstr(birthday)

def drawStars(stdscr, maxY, maxX):
    global starArray
    logging.debug("Max Y, X: %s, %s" % (maxY, maxX))
    for ittr in range(0, 100):
        randomY = random.randrange(maxY)
        randomX = random.randrange(maxX)
        starArray.append([randomY, randomX])
        stdscr.addch(randomY, randomX, curses.ACS_DIAMOND, curses.A_DIM)
    logging.debug("Array: %s", starArray)

def twinkleRandomStar(stdscr):
    global starArray
    for x in range(0, int(len(starArray) / 2)):
        randCoordinates = starArray[random.randrange(len(starArray))]
        if(random.random() > .5):
            stdscr.addch(randCoordinates[0], randCoordinates[1], curses.ACS_DIAMOND, curses.A_BOLD)
        else:
            stdscr.addch(randCoordinates[0], randCoordinates[1], curses.ACS_DIAMOND, curses.A_DIM)

def drawHeart(stdscr, maxY, maxX):
    logging.debug("Max Y, X: %s, %s" % (maxY, maxX))
    stdscr.addstr(heart)

def main():
    random.seed(time.time())
    logging.basicConfig(filename="gfl.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    maxY = stdscr.getmaxyx()[0];
    maxX = stdscr.getmaxyx()[1];

    heartWin = curses.newwin(38, 83, int((maxY / 2) - (38 / 2) + 4), int((maxX / 2) - (83 / 2)))
    birthdayWin = curses.newwin(7, 129, 0, int((maxX / 2) - (129/2)))
    try:
        drawStars(stdscr, maxY, maxX)
        while(True):
            drawHeart(heartWin, maxY, maxX)
            drawHappyBirthday(birthdayWin, maxY, maxX)
            stdscr.refresh()
            birthdayWin.refresh()
            heartWin.refresh()
            twinkleRandomStar(stdscr)
            time.sleep(.15)
            birthdayWin.erase()
            heartWin.erase()
    except KeyboardInterrupt:
        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    main()
