############################################################
# CMPSC/DS 442: Uninformed Search
############################################################

student_name = "Michael Tufillaro"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import math
import itertools
import random
import copy
from collections import deque

############################################################
# Section 1: N-Queens
############################################################

def num_placements_entire(n):
    # there are n indistinguishable queens and n^2 total spaces to put them, so there n^2 choose n possible placements
    return math.comb(n**2, n)


def num_placements_one_in_row(n):
    # if the only restriction you have is that there is one queen per row, then there are n different places to place a queen for each of the n rows
    return n**n


def n_queens_valid(board):
    # firstly, if the board list has the same number more than once, its automatically invalid
    # Create a set from the board values (removes any repeated values) and find its length
    numberOfUniqueValues = len(set(board))
    # If the set's length is different than board's length, then there's at least one repeated value and therefore the board is invalid
    if numberOfUniqueValues != len(board): return False
    # utilize helper function to check if diagonals make it invalid
    return diagonalChecker(board)


def diagonalChecker(board):
    n = len(board)
    # check all pairs of queens to see if any pairs violate the rule
    for i in range(0, n-1):
        for j in range(i+1, n):
            # Take the absolute value of the difference of any pair of indices and the absolute value of the difference of their values. 
            # If equal, they're on the same diagonal and therefore are invalid
            indexDif = abs(i-j)
            valueDif = abs(board[i]-board[j])
            if indexDif == valueDif: return False
    # if all diagonals are valid, then the board is valid
    return True


def n_queens_solutions(n):
    
    # this will store the current state of the board that is being tested
    currentBoard = []


    # recursive inner function that tries to place a queen into the given row
    def placeQueen(currentRow):

        # Base case: all rows are filled, it must be valid, so yield a copy of the current board
        if currentRow == n: yield currentBoard.copy()
        
        # otherwise, try to add a queen into the current row
        # loop through all possible columns for this row
        for currentColumn in range(n):
            # add the current column as the value for the current row
            currentBoard.append(currentColumn)
            # check to see if its a valid placement. if it is, then recursively call placeQueen again with an incremented row
            if n_queens_valid(currentBoard): yield from placeQueen(currentRow + 1)
            # after either the placement was invalid or that placement was already fully explored recursively, remove that queen from the board
            currentBoard.pop()
        # this level of the recursive function then ends, and it steps back


    # start the recursion from row 0 with 'yield from' (which yields everything that the recursive function yields)
    yield from placeQueen(0)

    '''
    # FOR TESTING PURPOSES- Brute force solution with time complexity O(n! * n)

    # use itertools to generate a list (length n) of all possible permutations of 0 --> n-1
    allPossiblePositions = list(itertools.permutations(range(n)))
    # if not on the same diagonal, its valid, so yield board
    for board in allPossiblePositions: 
        if diagonalChecker(board): yield board
    '''



############################################################
# Section 2: Lights Out
############################################################



class LightsOutPuzzle(object):

    def __init__(self, board):
        # stores the board and its dimensions in class variables
        self.board = board
        self.rows = len(board)
        self.columns = len(board[0])


    def get_board(self):
        return self.board


    # helper method that swaps a light corresponding to the given row and column
    def swapLight(self, row, col):
        if self.board[row][col] == True: self.board[row][col] = False
        else: self.board[row][col] = True


    def perform_move(self, row, col):
        # swap the given light
        self.swapLight(row, col)
        # check to see if it has each neighbor, and if it does, then swap it
        if row - 1 >= 0: self.swapLight(row - 1, col)
        if row + 1 < self.rows: self.swapLight(row + 1, col)
        if col - 1 >= 0: self.swapLight(row, col - 1)
        if col + 1 < self.columns: self.swapLight(row, col + 1)


    def scramble(self):
        # for every square, has a 50% chance to perform a move on it, functionally randomizing the state of the puzzle
        for row in range(self.rows):
            for column in range(self.columns):
                if random.random() < 0.5:
                    self.perform_move(row, column)


    def is_solved(self):
        # loop thru and return True if every value is False
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] == True: return False
        return True


    def copy(self):
        # uses copy.deepcopy to make a deep copy of the board(same values but referring to a different object)
        boardCopy = copy.deepcopy(self.board)
        return LightsOutPuzzle(boardCopy)


    def successors(self):
        # basically for every possible move you can make, display what the outcome would look like
        # loop through all values, and return the current coordinates (row, column) in a tuple with a copied board where that move was made on it
        listOfSuccessors = []

        for row in range(self.rows):
            for column in range(self.columns):
                # make a copy of the current object state, then perform the move corresponding to the current coordinates on it
                puzzleCopy = self.copy()
                puzzleCopy.perform_move(row, column)
                # add a tuple of the coordinates and the copy to the list of successors
                listOfSuccessors.append(((row, column), puzzleCopy))

        return listOfSuccessors


    # helper method that returns a tuple of tuples representation of the board state
    def boardToTuple(self):
        # call tuple method to turn each row in self.board into a tuple, and then turn the list of tuples into a tuple
        # this results in a tuple of tuples containing the board state, for use in determining if a state has already been visited
        return tuple(tuple(row) for row in self.get_board())


    def find_solution(self):
        # if the puzzle is already solved, return an empty list
        if self.is_solved(): return []
        
        # use deque as a frontier queue to do BFS- holds a tuple with a state and the path taken to get to that state
        # initialized with the starting state and empty list
        startingEntry = (self.copy(), [])
        frontier = deque([startingEntry])
        # create a set to contain the visited nodes, stored as tuples for the purposes of easy lookup
        # initialized with the starting state, in tuple form
        visited = {self.boardToTuple()}

        # loop as long as there are values left in the frontier
        while frontier:
            # pop out the oldest value from the frontier
            currentObject, currentPath = frontier.popleft()
            # call successors function on the current object to get all of its successors
            listOfSuccessors = currentObject.successors()
            
            # loop through all successors for the current object (all possible moves one could make)
            # nextCoordinates are the (row, column) tuple of the next move, and nextObject is what the current state would be if that move was done on it
            for nextCoordinates, nextObject in listOfSuccessors:
               # get the tuple representation of the current successor
               successorTuple = nextObject.boardToTuple()
               
               # if the state is one thats already been visited, ignore it and move on to next successor 
               if successorTuple in visited: continue
               
               # adds the previous path and the next step to get the path to the current successor
               pathToSuccessor = currentPath + [nextCoordinates]
               
               # if the successor is a solution, then return the path to get to it
               # Since its BFS, the first solution found is guaranteed to be (at least tied for) the most efficient (shallowest)
               if nextObject.is_solved(): return pathToSuccessor
               
               # if the successor hasn't been visited and isn't a solution, add it to the visited nodes and the queue
               visited.add(successorTuple)
               # frontier queue takes the next object and the path to get to it (the old path plus the new path)
               frontier.append((nextObject, pathToSuccessor))
            
        # if all frontier values have been explored and no solution was returned, then there are no solutions
        return None
        
    
    # helper function that prints out the current state of the board in a readable way for debugging purposes
    def printBoard(self):
        for row in range(self.rows):
            for column in range(self.columns):
                print(self.board[row][column], end = "\t")
            print("\n")
        print("\n")


def make_puzzle(rows, cols):
    board = []
    # Creates a 2D array of size (rows x cols) filled with False
    for row in range(rows):
        board.append([])
        for column in range(cols):
            board[row].append(False)
    # creates and returns a new LightsOutPuzzle with the specified size
    return LightsOutPuzzle(board)



############################################################
# Section 3: Linear Disk Movement
############################################################



class linearDiskPuzzle(object):

    def __init__(self, n, identical, grid):
        #stores the board and its dimensions in class variables
        self.length = len(grid)
        self.n = n
        self.identical = identical
        self.grid = grid
    

    # returns a tuple representation of the grid
    def gridToTuple(self):
        return tuple(self.grid)
    

    # returns a new linearDiskPuzzle with the same grid state
    def copy(self):
        copyOfGrid = copy.deepcopy(self.grid)
        return linearDiskPuzzle(self.n, self.identical, copyOfGrid)


    # helper method that determines whether the puzzle is solved
    def isSolved(self):
        # creates a reversed copy of the grid and loops through the first n values
        reversedGrid = self.grid[::-1]
        for i in range(self.n):
            # depending on if the disks are identical or not, there is a different metric for success
            if self.identical:
                # if any of the first n values are not 1, then it is not solved.
                if reversedGrid[i] != 1: return False
            else:
                # for the distinct disks, they need to be in the opposite order as they started. Therefore they must be in order at the start of the reversed grid.
                if reversedGrid[i] != i + 1: return False
        return True
    

    # helper method that attempts to move a disk from [fromIndex] to [toIndex]
    def makeMove(self, moveTuple):
        fromIndex = moveTuple[0]
        toIndex = moveTuple[1]
        # first need to check to see if the move is possible. Returns False if it is an invalid move or True if the move is valid (and is then made)

        # the value at fromIndex needs to be non-zero and the value at toIndex needs to be 0
        if self.grid[fromIndex] == 0 or self.grid[toIndex] != 0: return False

        # fromIndex either has to be next to toIndex or two indices away with a non-zero index between them
        distanceBetweenIndices = abs(fromIndex - toIndex)
        if (distanceBetweenIndices == 1) or (distanceBetweenIndices == 2 and self.grid[min(fromIndex, toIndex) + 1] != 0):
            # make move
            # if its a valid move, swap the values at fromIndex and toIndex and return True
            self.grid[fromIndex], self.grid[toIndex] = self.grid[toIndex], self.grid[fromIndex]
            return True
        
        return False


    # need to return all possible successors of the current grid, returning a tuple of the move made and what the grid looks like
    def successors(self):
        # in the form of ((from, to), linearDiskPuzzle)
        successorList = []
        # loop through the grid
        for i in range(self.length):
            # for any non-zero values, check to see if it can make any moves
            if self.grid[i] != 0:
                # loop from i-2 to i+2, aka the possible range any given piece can move (or less if theres not enough room)
                lowerBound = i-2
                if lowerBound < 0: lowerBound = 0
                # this is i + 3 because its not inclusive
                upperBound = i+3
                if upperBound > self.length: upperBound = self.length

                for j in range(lowerBound, upperBound):
                    # if there is an open spot within range
                    if self.grid[j] == 0:
                        # for each potential move, create a copy of the successor and try to make the move
                        puzzleCopy = self.copy()
                        # If the move was successful (makeMove returns True), add the copy to the successorList
                        if i != j and puzzleCopy.makeMove((i,j)):
                            successorList.append(((i,j), puzzleCopy))
        
        return successorList
    

    # implements a BFS algorithm to find the most efficient solution and return the steps taken to reach the solution
    # I structured the rest of this problem so that I could reuse my part 2 solution code with minimal adjustments, since that was also a BFS algorithm
    def solve(self):
        # if the puzzle is already solved, return an empty list
        if self.isSolved(): return []
        
        # use deque as a frontier queue to do BFS- holds a tuple with a state and the path taken to get to that state
        # initialized with the starting state and empty list
        startingEntry = (self.copy(), [])
        frontier = deque([startingEntry])
        # create a set to contain the visited nodes, stored as tuples for the purposes of easy lookup
        # initialized with the starting state, in tuple form
        visited = {self.gridToTuple()}

        # loop as long as there are values left in the frontier
        while frontier:
            # pop out the oldest value from the frontier
            currentObject, currentPath = frontier.popleft()
            # call successors function on the current object to get all of its successors
            listOfSuccessors = currentObject.successors()
            
            # loop through all successors for the current object (all possible moves one could make)
            # nextCoordinates are the (row, column) tuple of the next move, and nextObject is what the current state would be if that move was done on it
            for nextCoordinates, nextObject in listOfSuccessors:
               # get the tuple representation of the current successor
               successorTuple = nextObject.gridToTuple()
               
               # if the state is one thats already been visited, ignore it and move on to next successor 
               if successorTuple in visited: continue
               
               # adds the previous path and the next step to get the path to the current successor
               pathToSuccessor = currentPath + [nextCoordinates]
               
               # if the successor is a solution, then return the path to get to it
               # Since its BFS, the first solution found is guaranteed to be (at least tied for) the most efficient (shallowest)
               if nextObject.isSolved(): return pathToSuccessor
               
               # if the successor hasn't been visited and isn't a solution, add it to the visited nodes and the queue
               visited.add(successorTuple)
               # frontier queue takes the next object and the path to get to it (the old path plus the new path)
               frontier.append((nextObject, pathToSuccessor))
            
        # if all frontier values have been explored and no solution was returned, then there are no solutions
        return None
            

# function that creates a representation of the problem given the parameters
def createGrid(length, n, identical):
    grid = []
    for i in range(length):
        # if the puzzle calls for identical disks, put n 1's at the start of the grid followed by length-n 0's
        if identical:
            if i < n: grid.append(1)
            else: grid.append(0)
        # if the puzzle calls for distinct disks, put n values first where the value equals its index plus 1
        else:
            if i < n: grid.append(i+1)
            else: grid.append(0)
    return grid


def solveDisks(length, n, identical):
    # calls helper method to make a grid with the given length and n
    grid = createGrid(length, n, identical)
    # creates an instance of a linearDiskPuzzle object with the given parameters, and then solve it
    ldp = linearDiskPuzzle(n, identical, grid)
    return ldp.solve()


def solve_identical_disks(length, n):
    return solveDisks(length, n, identical = True)
    

def solve_distinct_disks(length, n):
    return solveDisks(length, n, identical = False)