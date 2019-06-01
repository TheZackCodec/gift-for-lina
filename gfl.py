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
from multiprocessing import Process
from playsound import playsound

heart = open('ascii/heart.txt', 'r').read()
birthday = open('ascii/birthday.txt', 'r').read()

starArray = []
prefetchArr = []
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

def playMusic():
    playsound('audio/Daulton Hopkins - Maroon.mp3')

def scene1(stdscr):
    heartWin = curses.newwin(38, 83, int((maxY / 2) - (38 / 2) + 4), int((maxX / 2) - (83 / 2)))
    birthdayWin = curses.newwin(7, 129, 0, int((maxX / 2) - (129/2)))

    drawStars(stdscr, maxY, maxX)
    epoch = time.time() + 29.6
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

def prefetchPhotos():
    global prefetchArr
    ittr = 1

    for dirpath, dirnames, files in os.walk('img/'):
        for file in files:
            img = Image.open("img/%s" % file)
            logging.debug('Image %s loaded with dimensions %s x %s' % (img.filename, img.size[0], img.size[1]))
            img = img.resize([int(img.size[0] / 2), int(img.size[1] / 2)], Image.BICUBIC)
            logging.debug('Image resized to %s x %s' % (img.size[0], img.size[1]))
            prefetchArr.append(img)
            ittr = ittr + 1

    logging.debug('prefetchArr Array: %s' % prefetchArr)

def slideShow1():
    global prefetchArr

    for x in range(0,7):
        prefetchArr[x].show()
        time.sleep(3.6)

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
        proc = Process(target=playMusic, name="Audio Player")
        prefetchPhotos()
        proc.start()
        time.sleep(15.6)
        scene1(stdscr)
        slideShow1()
        endSession()

    except KeyboardInterrupt:
        logging.warn("Keyboard Interrupt Event Detected...shutting down")
        endSession()

    except Exception as e:
        logging.error("%s" % e)
        endSession()
    finally:
        logging.warn("Killing Child Process %s with pid %s" % (proc.name, proc.pid))
        proc.terminate()

if __name__ == "__main__":
    main()
