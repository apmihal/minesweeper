import random
class Board:
    
    def __init__(self, size):
        self.size = size
        self.mines = size
        self.board = []
        self.mineList = []
        self.guesses = []
        self.zeroList = []
        self.flagList = []
        self.winList = []
        
        self.makeBoard()
        
    def makeBoard(self):
        """Generates a list of coordinates for all spaces of a board defined by self.size x self.size"""
        for i in range(self.size):
            for j in range(self.size):
                self.board.append([i, j])
                
        self.plantMines()
        
    def plantMines(self):
        """Randomly selects x and y values within the board to designate as mines. Only adds a mine if it's not a duplicate.
           Stops when a preset number of mines have been created. By default that number is the same as self.size""" 
        while len(self.mineList) < self.mines:
            randx = random.randrange(0, self.size)
            randy = random.randrange(0, self.size)
            if [randx, randy] not in self.mineList:
                self.mineList.append([randx, randy])

        self.makeWinList()
                
    def makeWinList(self):
        for i in range(self.size):
            for j in range(self.size):
                if [i, j] not in self.mineList:
                    self.winList.append([i, j])
        
    def isMine(self, guessx, guessy):
        """Returns true or false depending on whether a given coord is in self.mineList"""
        if [guessx, guessy] in self.mineList:
            return True
        else:
            return False
            
    def minesTouching(self, x, y):
        """Looks around a given coord for mines, and increases a counter for each found"""
        touching = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if [x + i, y + j] != [x, y] and [x + i, y + j] in self.mineList:
                    touching += 1
        
        return touching
            
    def guess(self, guessx, guessy):
        """Adds a guess to the list off guesses, but if it's a blank space, begins the rippling process of revealing adjacent blank
            spaces."""
        if self.minesTouching(guessx, guessy) > 0 and [guessx, guessy] not in self.guesses:
            self.guesses.append([guessx, guessy])
        else:
            if [guessx, guessy] not in self.guesses:
                self.guesses.append([guessx, guessy])
            if [guessx, guessy] not in self.zeroList:
                self.zeroList.append([guessx, guessy])
            # Iterates through a list of blank spaces (zeroes) as it is building it's list of blank spaces
            for item in self.zeroList:
                self.ripple(item[0], item[1])
                
    def ripple(self, x, y):
        """Clears all adjacent blank spaces"""
        # look around coord
        for i in range(-1, 2):
            for j in range(-1, 2):
                # add all zero/blank spaces it finds to both the zeroList and to the guesses list.
                if self.minesTouching(x + i, y + j) == 0 and [x + i, y + j] not in self.zeroList:
                    if [x + i, y + j] not in self.guesses:
                        self.guesses.append([x + i, y + j])
                    # checks if it's on the board. without this line, this code starts searching every coord possible
                    if [x + i, y + j] in self.board:
                        self.zeroList.append([x + i, y + j])
                # If it's not a zero, adds all other numbered spots it find to the guess list.
                if [x + i, y + j] not in self.mineList and [x + i, y + j] not in self.guesses:
                    if [x + i, y + j] in self.board:
                        self.guesses.append([x + i, y + j])

    def printBoard(self):
        """Formatted print statements to print out the game board in it's current state."""
        print("  ", end="")
        for _ in range(self.size):
            print(_, "", end="")
        print()
        for i in (range(self.size)):
            print(i, "", end="")
            for j in (range(self.size)):
                print(self.spaceState(i, j), "", end="")
                
            print()
            
    def printLosingBoard(self):
        print("  ", end="")
        for _ in range(self.size):
            print(_, "", end="")
        print()
        for i in (range(self.size)):
            print(i, "", end="")
            for j in (range(self.size)):
                print(self.losingSpaceState(i, j), "", end="")
                
            print()
        
 
    def spaceState(self, x, y):
        """Determines which symbol should be printed when printing the board."""
        if [x, y] in self.flagList:
            return '╕'
        elif [x, y] in self.guesses and [x, y] not in self.mineList:
            if self.minesTouching(x, y) == 0:
                return ' '
            return self.minesTouching(x, y)
        elif [x, y] in self.guesses and [x, y] in self.mineList:
            return '÷'
        else:
            return '÷'
                
    def losingSpaceState(self, x, y):
        """Reveals values of all spaces and locations of mines when swapped out for spaceState in printBoard"""
        if [x, y] in self.flagList:
            return '╕'
        elif self.isMine(x, y):
            return '*'
        elif [x, y] in self.guesses:
            if self.minesTouching(x, y) == 0:
                return ' '
            return self.minesTouching(x, y)
        else:
            return '÷'
                   
    def addFlag(self, x, y):
        if [x, y] not in self.flagList:
            self.flagList.append([x, y])
        
    def removeFlag(self, x, y):
        if [x, y] in self.flagList:
            self.flagList.remove([x, y])
        
    def isWon(self):
        """Checks to see if all of the non-mine square have been revealed."""
        for i in self.winList:
            if i not in self.guesses:
                return False
                
        return True
        
    def validateCoordInput(self, ask, error):
        valid = False
        while not valid:
            
            value = -1
            while value >= self.size or value < 0:
                try:
                    value = int(input(ask))
                    if value >= self.size or value < 0:
                        print(error)
                    else:
                        valid = True
                except ValueError:
                    print(error)
                    
        return value
                
def printLogo():
    print(' ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗')
    print('██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗')
    print('██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║')
    print('██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║')
    print('╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝')
    print(' ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝')
    print('██╗     ██╗███╗   ██╗███████╗███████╗██╗    ██╗███████╗███████╗██████╗ ███████╗██████╗ ')
    print('██║     ██║████╗  ██║██╔════╝██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗')
    print('██║     ██║██╔██╗ ██║█████╗  ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝█████╗  ██████╔╝')
    print('██║     ██║██║╚██╗██║██╔══╝  ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗')
    print('███████╗██║██║ ╚████║███████╗███████║╚███╔███╔╝███████╗███████╗██║     ███████╗██║  ██║')
    print('╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝')
    print('Created by Andrew Mihalevich and based on the classic game Crash Bandicoot 2: Cortex Strikes Back.')
    
def validateInput(ask, error):
    valid = False
    while not valid:
        try:
            value = int(input(ask))
            valid = True
        except ValueError:
            print(error)
            
    return value
    
def main():
    printLogo()
    input('Press enter to contiune')
    #size = validateInput('How big should the game board be? ', 'Please enter an integer. ')
    minesweeper = Board(10)
    game_over = False
    while not game_over and not minesweeper.isWon():
        minesweeper.printBoard()
        answered = False
        while not answered:
            action = input('Whould you like to add or remove flag, or guess? Type "add" "remove" or "guess". ')
            if action == 'add':
                x = minesweeper.validateCoordInput('Which row would you like to select? ', 'That is not a valid row. ')
                y = minesweeper.validateCoordInput('Which column would you like to select? ', 'That is not a valid column. ')
                minesweeper.addFlag(x, y)
                answered = True
            elif action == 'remove':
                x = minesweeper.validateCoordInput('Which row would you like to select? ', 'That is not a valid row. ')
                y = minesweeper.validateCoordInput('Which column would you like to select? ', 'That is not a valid column. ')
                minesweeper.removeFlag(x, y)
                answered = True
            elif action == 'guess':
                x = minesweeper.validateCoordInput('Which row would you like to select? ', 'That is not a valid row. ')
                y = minesweeper.validateCoordInput('Which column would you like to select? ', 'That is not a valid column. ')
                minesweeper.guess(x, y)
                game_over = minesweeper.isMine(x, y)
                answered = True
            else:
                print('Please enter "add flag" "remove flag" or "guess". ')

    if minesweeper.isWon():
        minesweeper.printBoard()
        print('You win!')
    else:
        minesweeper.printLosingBoard()
        print('BOOM')

if __name__ == '__main__':
    main()


