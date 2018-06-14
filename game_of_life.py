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

# game space (universe for the cell population
universe = [[0 for y in range(width)] for x in range(height)]
next_universe = [[0 for y in range(width)] for x in range(height)]


def main(stdscr):

    global live, dead

    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    curses.cbreak()
    curses.noecho()

    stdscr.addstr(0, 0, '---------------------------')
    stdscr.addstr(1, 0, '       Game of life')
    stdscr.addstr(2, 0, '---------------------------')

    # Users may define the live and dead cells
    get_symbol(stdscr, 'live', 3)

    get_symbol(stdscr, 'dead', 5)

    init_universe(universe)

    # Users may pick a number of seeds or their own
    get_seeds(stdscr)

    stdscr.refresh()
    time.sleep(1)

    # GOL is displayed on the terminal
    while True:
        stdscr.clear()

        show_universe(stdscr)
        stdscr.addstr(height+2, 0, 'Enter x to exit.  Enter any other key to continue to next round')

        # GOL goes on
        propagate(stdscr)

        key = chr(stdscr.getch())
        if (key == 'x'):   # 'x' exits the game
            exit()

        else:
        # elif (key == curses.ascii.SP):  # next round
            continue

def propagate(stdscr):

    global universe, next_universe

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
                # Overpopulation
                elif neighbors > 3:
                    next_universe[i][j] = dead

                logging.debug('{}->{}'.format(universe[i][j], next_universe[i][j]))
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
        stdscr.addstr(17, 0, 'game over')


def count_neighbors(univ, y, x, stdscr):

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

    # if univ[i][j] == live:
    #     neighbor_count -= 1

    # stdscr.addstr(19, 0, str(neighbor_count))
    if neighbor_count:
        message = '@ {}-{}-{}:{}-{}-{} count {}'.format(y_min, y, y_max, x_min, x, x_max, neighbor_count)
        logging.debug(message)

    return neighbor_count


def get_manual_seeds(stdscr):

    global height, width
    show_universe(stdscr)

    stdscr.addstr(height + 2, 0, 'Use keyboard to move.  Enter s to place a seed. Enter q to exit. ')
    stdscr.addstr(height + 3, 0, 'a / d for left / right, w / x for up / down.')

    x = 0
    y = 0

    key = ''

    while key != 'q':
        key = chr(stdscr.getch())

        if key == 'q': # Finish
            stdscr.clear()
            return

        elif key == 'a': # Left
            if x == 0:
                x = width - 1
            else:
                x = x - 1

        elif key == 'd': # Right
            if x >= width-1:
                x = 0
            else:
                x = x + 1

        elif key == 'w': # Up
            if y == 0:
                y = height - 1
            else:
                y = y - 1

        elif key == 'x': # Down
            if y >= height-1:
                y = 0
            else:
                y = y + 1

        # curses.setsyx(y, x)

        if key == 's': # Place Seed
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

    stdscr.addstr(7, 0, 'How many seeds would you like to randomly place?')
    stdscr.addstr(8, 0, 'Enter a number between 1 and 9 or 0 for manual placement: ')

    seeds = stdscr.getch()

    stdscr.clear()

    if curses.ascii.isdigit(seeds):
        stdscr.refresh()

    if seeds >= 49 and seeds <= 57:
        stdscr.addstr(9, 0, 'Randomly placing {} seeds'.format(seeds-48))
        random_seeds(seeds-48)

    elif seeds == 48:
        stdscr.addstr(9, 0, 'Manual input selected')
        get_manual_seeds(stdscr)

    else:
        stdscr.addstr(9, 0, 'Sorry, wrong input')
        exit()

    stdscr.clear()


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

    stdscr.addstr(y, 0, 'Enter a symbol for a {} cell: '.format(target))
    c = stdscr.getch()

    if curses.ascii.isalnum(c):
        stdscr.addstr(y+1, 0, chr(c))
        if target == 'live':
            live = chr(c)
        elif target == 'dead':
            dead = chr(c)


if __name__ == '__main__':
    curses.wrapper(main)