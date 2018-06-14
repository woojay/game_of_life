    ### Game of Life ###
    
    ## Objective: ##
    You'll implement Conway's Game of Life (https://en.wikipedia.org/wiki/Conway's_Game_of_Life) as a CLI tool.

    ## Criteria: ##
    Conway's Game of Life is displayed in the terminal.
    Conway's Game of Life plays indefinitely until a user terminates.
    Users may pick a number of starting states(seeds) or enter their own.
    Users may define the appearance of live and dead cells.

    ## Instruction:## 

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