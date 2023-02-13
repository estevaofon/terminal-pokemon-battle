import curses
import time

__author__ = "Estêvão Fonseca"
class Tamagotchi:
    def __init__(self):
        self.life = 100
        self.evolved = False


tamagotchi = Tamagotchi()
fed = time.time()
born = time.time()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    height, width = stdscr.getmaxyx()
    win = curses.newwin(20, 60, 0, 0)
    win.bkgd(' ', curses.color_pair(1))

    while True:
        stdscr.keypad(True)
        stdscr.nodelay(True)
        c = stdscr.getch()
        idle(win)

def idle(win):
    win.refresh()
    win.addstr(2, 1, "(=^ .^=) ")
    win.refresh()
    time.sleep(0.5)
    win.addstr(2, 1, "(= '.'=)")
    win.refresh()
    time.sleep(0.5)



curses.wrapper(main)