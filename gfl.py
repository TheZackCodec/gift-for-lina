##############################################
#   Author: Derick Vigne
#   Todo:
#   - Organize into story pages or phases
#
##############################################

import os, sys
import logging
import time
import curses
from PIL import Image
from multiprocessing import Process
from support import support

prefetchArr = []

def endSession():
    logging.debug('Ending Session')
    curses.curs_set(1)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def prefetchPhotos():
    global prefetchArr
    ittr = 1

    for dirpath, dirnames, files in os.walk('img/'):
        for file in range(1, len(files)):
            img = Image.open("img/%s.jpg" % file)
            logging.debug('Image %s loaded with dimensions %s x %s' % (img.filename, img.size[0], img.size[1]))
            img = img.resize([int(img.size[0] / 2), int(img.size[1] / 2)], Image.BICUBIC)
            logging.debug('Image resized to %s x %s' % (img.size[0], img.size[1]))
            prefetchArr.append(img)
            ittr = ittr + 1

    logging.debug('prefetchArr Array: %s' % prefetchArr)

def main():
    logging.basicConfig(filename="gfl.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    maxY = stdscr.getmaxyx()[0]
    maxX = stdscr.getmaxyx()[1]

    logging.debug("Max Y, X: %s, %s" % (maxY, maxX))

    scenes = support(maxY, maxX)

    try:
        scenes.playMusic()
        # logging.debug('Process %s with PID %s started' % (proc.name, proc.pid))
        scenes.heartBeats(stdscr)
        scenes.scene1(stdscr)
        scenes.scene2(stdscr)
        scenes.scene3(stdscr)
        scenes.slideShow1(prefetchArr)
        # scenes.scene4(stdscr)
        endSession()

    except KeyboardInterrupt:
        logging.warn("Keyboard Interrupt Event Detected...shutting down")
        endSession()

    except Exception as e:
        logging.error("%s" % e)
        endSession()
    finally:
        logging.warning("Killing Child Process %s with pid %s" % (proc.name, proc.pid))
        proc.terminate()

if __name__ == "__main__":
    main()
