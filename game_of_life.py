'''
    Game of Life CLI version

    by wp
    6/13/18

    Objective:
    You'll implement Conway's Game of Life (https://en.wikipedia.org/wiki/Conway's_Game_of_Life) as a CLI tool.

    Criteria:
    Conway's Game of Life is displayed in the terminal.
    Conway's Game of Life plays indefinitely until a user terminates.
    Users may pick a number of starting states(seeds) or enter their own.
    Users may define the appearance of live and dead cells.

    Instruction:

    - Setup
    0.  '(sudo) pip install curses' if needed
    1.  'python game_of_life.py' in either python 3.6.4 or 2.7.14 (linux only)

    - Game Play
    0.  I used pyenv to test py 3.6.4 and py 2.7.14 environements, FYI
    1.  Enter a single character to represent a live cell. Any alpha-numeric is great.
    2.  Enter a single character to represent a dead cell.  '.' works well.
    3.  Highly recommend to enter '0' to select manually.  Selecting between 1-9 is highly likely to all die in the
        first round.
    4.  10x40 grid will show up, which is the 'universe.'  You can move around the position w/ a, d, w, and x keys.
    5.  Once located, enter 's' to place a seed.  Do as many as you like, and enter 'q' to exit the set up mode.
    6.  Once exited, the each round is run after a single keyboard input other than 'x'.  Each key press will represent
        a single round.
    7.  If all the cells die, 'game over' message will show, but will not exit unless a single 'x' is entered.
    8.  'x' will always exit the simulation rounds.
    9.  In case of a 'still life,' no special message will show even though each round will return a same outcome.
    10. Hope this makes sense to you.  Thank you so much.


'''

import curses
import curses.ascii
import time
import random
import logging


# User selectable live / dead cell symbols
live = 'O'
dead = '.'

# global screen size of cell universe
height=10
width=40

# game space (universe for the cell population)
universe = [[0 for y in range(width)] for x in range(height)]

def main(stdscr):
    '''
    Main Game Logic
    :param stdscr: screen
    '''

    # global live, dead

    logging.basicConfig(filename='log.log', level=logging.ERROR)
    # logging.basicConfig(filename='log.log', level=logging.DEBUG)

    curses.cbreak()
    curses.noecho()

    # Welcome / instruction screens
    show_intro(stdscr)
    show_banner(stdscr)

    # Users may define the live and dead cells
    get_symbol(stdscr, 'live', 3)
    get_symbol(stdscr, 'dead', 5)

    # Get game space ready
    init_universe(universe)

    # Users may pick a number of seeds or their own
    get_seeds(stdscr)
    stdscr.refresh()
    time.sleep(1)

    # GOL is displayed on the terminal
    while True:
        stdscr.clear()

        # Show current state of universe
        show_universe(stdscr)
        stdscr.addstr(height+2, 0, 'Enter x to exit.  Enter any other key to continue to next round')

        # GOL goes on to next round
        propagate(stdscr)

        # Wait for a key to progress to next round or x for exiting the simulation
        key = chr(stdscr.getch())
        if (key == 'x'):   # 'x' exits the game
            exit()


def show_banner(stdscr):

    stdscr.addstr(0, 0, '---------------------------')
    stdscr.addstr(1, 0, '       Game of life')
    stdscr.addstr(2, 0, '---------------------------')


def show_intro(stdscr):

    stdscr.clear()
    show_banner(stdscr)

    stdscr.addstr(4, 0, 'Welcome!')

    stdscr.addstr(6, 0, 'The Conway\' Game of Life is rather a cellular automaton where you')
    stdscr.addstr(7, 0, 'start with initial set of cells you can manually or randomly place.')

    stdscr.addstr(9, 0, 'The rules of the game are as follows:')
    stdscr.addstr(10, 0, "For a space that is 'live' or 'populated':")
    stdscr.addstr(11, 0, '  Each cell with one or no neighbors dies, as if by solitude.')
    stdscr.addstr(12, 0, '  Each cell with four or more neighbors dies, as if by overpopulation.')
    stdscr.addstr(13, 0, '  Each cell with two or three neighbors survives.')
    stdscr.addstr(14, 0, "For a space that is 'dead' or 'empty'")
    stdscr.addstr(15, 0, '  Each cell with three neighbors becomes populated.')

    stdscr.addstr(17, 0, 'On the next screen, you will start by selecting your preferred symbol')
    stdscr.addstr(18, 0, 'to represent populated cells and empty cells.')

    stdscr.addstr(20, 0, 'When ready, please hit spacebar to continue.')

    # Wait for a keyboard input to move on
    while True:
        c = stdscr.getch()

        if chr(c) == ' ':
            break

    stdscr.clear()


def propagate(stdscr):
    '''
    Runs a single round of simulation
    :param stdscr: screen
    '''

    global universe

    next_universe = [[0 for y in range(width)] for x in range(height)]

    cell_count = 0

    init_universe(next_universe)

    for i in range(height):
        for j in range(width):
            # stdscr.addstr(i, j, universe[i][j])

            # Count number of neighbors
            neighbors = count_neighbors(universe, i, j, stdscr)

            # If live, and;
            if universe[i][j] == live:
                # Starvation
                if neighbors < 2:
                    next_universe[i][j] = dead
                # Move on but stay the same
                elif neighbors == 2 or neighbors == 3:
                    next_universe[i][j] = live
                    cell_count += 1
                    logging.debug('{}->{}'.format(universe[i][j], next_universe[i][j]))
                # Overpopulation
                elif neighbors > 3:
                    next_universe[i][j] = dead

            # if Dead
            elif universe[i][j] == dead:
                # Reproduction
                if neighbors == 3:
                    next_universe[i][j] = live
                    cell_count += 1
                    logging.debug('{}->{}'.format(universe[i][j], next_universe[i][j]))

    # copy over
    for i in range(height):
        for j in range(width):
            universe[i][j] = next_universe[i][j]

    if cell_count == 0:
        stdscr.addstr(17, 0, 'No more cells left.')


def count_neighbors(univ, y, x, stdscr):
    '''
    Determines the number of populated cells around a target cell
    :param univ: Target array universe
    :param y: Row
    :param x: Column
    :param stdscr: screen
    '''
    global height, width

    # Y Minimum
    if y <= 1:
        y_min = 0
    else:
        y_min = y - 1

    # Y Maximum
    if y >= height - 2:
        y_max = height - 1
    else:
        y_max = y + 1

    # X Minimum
    if x <= 1:
        x_min = 0
    else:
        x_min = x - 1

    # X Maximum
    if x >= width - 2:
        x_max = width - 1
    else:
        x_max = x + 1

    neighbor_count = 0
    for i in range(y_min, y_max+1):
        for j in range(x_min, x_max+1):
            if i == y and j == x:
                continue
            if univ[i][j] == live:
                neighbor_count += 1

    if neighbor_count:
        message = '@ {}-{}-{}:{}-{}-{} count {}'.format(y_min, y, y_max, x_min, x, x_max, neighbor_count)
        logging.debug(message)

    return neighbor_count


def get_manual_seeds(stdscr):
    '''
    Receive user's manual seed placements w/ keyboard input
    :param stdscr: screen
    '''

    global height, width, universe

    show_universe(stdscr)

    stdscr.addstr(height + 2, 0, 'Use arrow keys to move.  Enter a space to place a seed. Hit END key to finish. ')

    x = 0
    y = 0

    key = ''

    while True:
        key = stdscr.getch()

        if key == curses.KEY_END: # END to finish entering
            stdscr.clear()
            return

        elif key == curses.KEY_LEFT: # Left
            if x == 0:
                x = width - 1
            else:
                x = x - 1

        elif key == curses.KEY_RIGHT: # Right
            if x >= width-1:
                x = 0
            else:
                x = x + 1

        elif key == curses.KEY_UP: # Up
            if y == 0:
                y = height - 1
            else:
                y = y - 1

        elif key == curses.KEY_DOWN: # Down
            if y >= height-1:
                y = 0
            else:
                y = y + 1

        if chr(key) == ' ': # Place Seed
            stdscr.addstr(y, x, live)
            stdscr.addstr(y, x, '')     # Moves back the cursor after write
            universe[y][x] = live

        else:
            stdscr.addstr(y, x, '')

        stdscr.refresh()


def get_seeds(stdscr):
    '''
    Initial setup for seed placement in the game space (universe)
    :param stdscr: screen
    '''

    while True:
        stdscr.addstr(7, 0, 'How would you like to place initial cells?')
        stdscr.addstr(8, 0, 'Enter a number between 1 and 9 for 10 to 90 random seeds -OR-')
        stdscr.addstr(9, 0, '0 to place your own: ')

        seeds = stdscr.getch()

        stdscr.clear()

        if curses.ascii.isdigit(seeds):
            stdscr.refresh()

        if seeds >= 49 and seeds <= 57:
            seeds_count = (seeds - 48) * 10
            stdscr.addstr(10, 0, 'Randomly placing {} seeds'.format(seeds_count))
            random_seeds(seeds_count)
            break

        elif seeds == 48:
            stdscr.addstr(10, 0, 'Manual input selected')
            get_manual_seeds(stdscr)
            break

        else:
            stdscr.addstr(10, 0, 'Sorry, wrong input.  Please try again.')
            # time.sleep(1)


def clear_display(stdscr):
    '''
    Clears display window
\    '''

    height, width = stdscr.getmaxyx()

    blankline = ' ' * (width-1)

    for line in range(height):
        stdscr.addstr(line, 0, blankline)


def init_universe(univ):
    '''
    Clears universe data for live and dead cells
    '''

    for i in range(height):
        for j in range(width):
            univ[i][j] = dead


def random_seeds(seeds):
    '''
    Adds a few random seeds based on input
    :param seeds: number of seeds to add
    '''
    for seed in range(seeds):
        rand_y = random.randint(0, height-1)
        rand_x = random.randint(0, width-1)

        while (universe[rand_y][rand_x] != dead):
            rand_y = random.randint(0, height-1)
            rand_x = random.randint(0, width-1)

        universe[rand_y][rand_x] = live


def show_universe(stdscr):
    '''
    Displays the game space (universe)
    :param stdscr:
    '''
    for i in range(height):
        for j in range(width):
            stdscr.addstr(i, j, universe[i][j])


def get_symbol(stdscr, target, y):
    '''
    Gets user customized symbols for either live or dead cells for display
    :param stdscr: screen
    :param target: live or dead cell
    :param y: display height for screen
    '''

    global dead, live

    while True:

        if target == 'live':
            stdscr.addstr(y, 0, 'Enter an alphanumeric key to indicate a {} cell: '.format(target))
            c = stdscr.getch()

            if curses.ascii.isalnum(c):
                stdscr.addstr(y + 1, 0, chr(c) + ' is selected.                       ')
                live = chr(c)
                break
            else:
                stdscr.addstr(y + 1, 0, 'Only alphanumeric symbol is allowed.')

        elif target == 'dead':
            stdscr.addstr(y, 0, 'Enter an alphanumeric key or space to indicate a {} cell: '.format(target))
            c = stdscr.getch()

            if curses.ascii.isalnum(c) or chr(c) == ' ':
                stdscr.addstr(y + 1, 0, chr(c) + ' is selected.                       ')
                dead = chr(c)
                break
            else:
                stdscr.addstr(y + 1, 0, 'Only alphanumeric symbol or space is allowed.')


if __name__ == '__main__':
    curses.wrapper(main)
