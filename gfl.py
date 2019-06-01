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
from PIL import Image

heart = open('ascii/heart.txt', 'r').read()
birthday = open('ascii/birthday.txt', 'r').read()

starArray = []
maxY = None
maxX = None

def drawHappyBirthday(stdscr):
    stdscr.addstr(birthday)

def drawStars(stdscr, maxY, maxX):
    global starArray
    for ittr in range(0, 100):
        randomY = random.randrange(maxY)
        randomX = random.randrange(maxX)
        starArray.append([randomY, randomX])
        stdscr.addch(randomY, randomX, curses.ACS_DIAMOND, curses.A_DIM)
    logging.debug("Star Array: %s", starArray)

def twinkleRandomStar(stdscr):
    global starArray
    for x in range(0, int(len(starArray) / 2)):
        randCoordinates = starArray[random.randrange(len(starArray))]
        if(random.random() > .5):
            stdscr.addch(randCoordinates[0], randCoordinates[1], curses.ACS_DIAMOND, curses.A_BOLD)
        else:
            stdscr.addch(randCoordinates[0], randCoordinates[1], curses.ACS_DIAMOND, curses.A_DIM)

def drawHeart(stdscr):
    stdscr.addstr(heart)

def endSession():
    logging.debug('Ending Session')
    curses.curs_set(1)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def scene1(stdscr):
    heartWin = curses.newwin(38, 83, int((maxY / 2) - (38 / 2) + 4), int((maxX / 2) - (83 / 2)))
    birthdayWin = curses.newwin(7, 129, 0, int((maxX / 2) - (129/2)))

    drawStars(stdscr, maxY, maxX)
    epoch = time.time() + 5
    while(time.time() < epoch):
        drawHeart(heartWin)
        drawHappyBirthday(birthdayWin)
        stdscr.refresh()
        birthdayWin.refresh()
        heartWin.refresh()
        twinkleRandomStar(stdscr)
        time.sleep(.15)
        birthdayWin.erase()
        heartWin.erase()

def slideShow1():
    for x in range(1, 20):
        img = Image.open('img/%s.jpg' % x)
        logging.debug('Image %s loaded with dimensions %s x %s' % (img.filename, img.size[0], img.size[1]))
        img = img.resize([int(img.size[0] / 2), int(img.size[1] / 2)], Image.BICUBIC)
        logging.debug('Image resized to %s x %s' % (img.size[0], img.size[1]))
        img.show()
        time.sleep(1)
    os.system('dialog --msgbox "Continue..." 10 50')
    os.system('pkill display')

def main():
    global maxY, maxX
    random.seed(time.time())
    logging.basicConfig(filename="gfl.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    maxY = stdscr.getmaxyx()[0]
    maxX = stdscr.getmaxyx()[1]

    logging.debug("Max Y, X: %s, %s" % (maxY, maxX))


    try:
        scene1(stdscr)
        slideShow1()
        endSession()

    except KeyboardInterrupt:
        logging.warn("Keyboard Interrupt Event Detected...shutting down")
        endSession()
    except:
        logging.error("%s" % sys.exc_info()[0])
        endSession()

if __name__ == "__main__":
    main()
