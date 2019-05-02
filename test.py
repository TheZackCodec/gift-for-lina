import os, sys
import logging
import random
import time
import curses

star = "✧"
heart = """
 ____
 |  /
  |/\\_\\_
      \\_\\_
        \\_\\_
          \\.\\---..__             __..---,._
       .,'          "-.       .-"          `,.
     ,'                `.   .'                `,
    /                   `,_,'                      \\
   |                                             |
   ;                                             ;
    ;                                           ;
     `,                                       ,'
      `,                                      ,'
       `,                                  ,'
        `,                                ,'
         `,                              ,'
           `,                          ,'
             `,                     \\_\\_
               `,                   ,'\\_\\_
                 `,               ,'    \\_\\_
                   `,           ,'        \\+--
                     `,       ,'           | +--
                       `,   ,'               | +--
                         "-"
"""

def drawScreen(stdscr):
    maxY = stdscr.getmaxyx()[0]
    maxX = stdscr.getmaxyx()[1]
    logging.debug("Max Y, X: %s, %s" % (maxY, maxX))
    while(True):
        stdscr.erase()
        for ittr in range(0, maxX):
            stdscr.addch(random.randrange(maxY), random.randrange(maxX), star)
            time.sleep(.1)
            stdscr.refresh()

def drawHeart(stdscr):
    maxY = stdscr.getmaxyx()[0]
    maxX = stdscr.getmaxyx()[1]
    logging.debug("Max Y, X: %s, %s" % (maxY, maxX))
    stdscr.erase()
    stdscr.addstr(heart)
    while(True):
        stdscr.refresh()
def main():
    random.seed(time.time())
    logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    try:
        drawScreen(stdscr)
    except KeyboardInterrupt:
        curses.curs_set(1)
        curses.nocbreak()
        curses.endwin()


if __name__ == "__main__":
    main()
