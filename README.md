# Game of Life #

## Objective: ##
You'll implement Conway's Game of Life (https://en.wikipedia.org/wiki/Conway's_Game_of_Life) as a CLI tool.

## Criteria: ##
Conway's Game of Life is displayed in the terminal.
Conway's Game of Life plays indefinitely until a user terminates.
Users may pick a number of starting states(seeds) or enter their own.
Users may define the appearance of live and dead cells.

## Instruction: ## 

- Setup
0.  '(sudo) pip install curses' if needed
1.  'python game_of_life.py' in either python 3.6.4 or 2.7.14 (linux only)

- Game Play
0.  I used pyenv to test py 3.6.4 and py 2.7.14 environements, FYI
1.  Enter a single character to represent a live cell. Any alpha-numeric is great.
2.  Enter a single character to represent a dead cell.  ' ' or '.' works well.
3.  Enter '0' to select manual seed entry or select between 1-9 to randomly place 10 to 90 seeds.
4.  For manual entry, 10x40 grid will show up, which is the 'universe.'  You can move around the cursor position with arrow keys.
    Hit space to place a seed.  Do as many as you like, and hit END key to exit the set up mode.
5.  Once set up, the each round is run after a single keyboard input other than 'x'.  Each key press will represent
    a single round.
6.  If all the cells die, a message will show, but will not exit unless a single 'x' is entered.
7.  'x' will always exit the simulation rounds.
8.  In case of a 'still life,' no special message will show even though each round will return a same outcome.
9.  Hope this makes sense to you.  Thank you so much.
