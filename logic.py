import numpy as np
import random

"""
Created on Fri Nov 20 02:24:44 2020

@author: caseyquinn
"""


def valid_moves(board):
    """function takes in as parameter the connect 4 board and checks for available moves
    in which a person can make a move in the game"""
    # -only need to examine first row of the board so slice the board and create a list that only contains the
    #  first row (create first row variable)
    first_row = board[0][:]
    # create an empty list in which available column numbers will be appended if a move can be made there
    available_columns = []
    # -set column counter variable so as we iterate through the list we can increment the column number that would
    # be appended to available columns list
    columncounter = 0
    # -loop through the first row and find any available moves
    for i in first_row:
        # if i is zero, a move can be made in that column
        if i == 0:
            i = columncounter  # set i equal to column counter so that can be appended to the list
            available_columns.append(columncounter)  # append to the list
        columncounter += 1  # increment the column counter

    # return the available columns list
    return available_columns


def valid_move(column, board):
    return column in valid_moves(board)


def check_horizontals(board):
    """function takes in connect four board as parameter and checks if there is a horizontal winner"""
    # create variable that keeps track of the row number if there is a winner that will be returned
    rownumber = 0
    # initiate empty list local variable that will be used to store the index numbers of the row where there is a winner
    indexnums = []
    # iterate through the board using a for loop and check each row in the board for a horizontal win
    for row in board:
        # increment the row number
        rownumber += 1
        # -check each row for combination where 1 wins
        # -there are 4 possibilities to win in each row
        # -slice each row at appropriate places to represent each possibility within a single row and use
        # conditionals to see if there is a win
        # -use break statement to break out of loop if there is a winner
        if row[:4] == [1, 1, 1, 1]:  # winner is 1
            winner = 1
            indexnums = [0, 1, 2, 3]  # element nums 0-3
            break
        elif row[1:5] == [1, 1, 1, 1]:  # winner is 1
            winner = 1
            indexnums = [1, 2, 3, 4]  # element nums 1-4
            break
        elif row[2:6] == [1, 1, 1, 1]:  # winner is 1
            winner = 1
            indexnums = [2, 3, 4, 5]  # element nums 2-5
            break
        elif row[3:] == [1, 1, 1, 1]:  # winner is 1
            winner = 1
            indexnums = [3, 4, 5, 6]  # element nums 3-6
            break
        # check each row for same combinations but see if 2 wins
        elif row[:4] == [2, 2, 2, 2]:  # winner is 2
            winner = 2
            indexnums = [0, 1, 2, 3]  # element nums 0-3
            break
        elif row[1:5] == [2, 2, 2, 2]:  # winner is 2
            winner = 2
            indexnums = [1, 2, 3, 4]  # element nums 1-4
            break
        elif row[2:6] == [2, 2, 2, 2]:  # winner is 2
            winner = 2
            indexnums = [2, 3, 4, 5]  # element nums 2-5
            break
        elif row[3:] == [2, 2, 2, 2]:  # winner is 2
            winner = 2
            indexnums = [3, 4, 5, 6]  # element nums 3-6
            break
        # if winner is not 1 or 2 then there is no winner
        else:
            winner = 0
    # if no winner is found then rownumber is reassigned as 0 and winner = 0 is returned
    if winner == 0:
        rownumber = 0
        return winner
    else:
        # return tuple containing winner, row number, index nums if there is a winner
        return winner, rownumber, indexnums


def transpose(board):
    """function will transpose the connect 4 board which will enable check vertical function to
    check vertical wins"""
    # create a list for each column on the board
    columns = [[] for _ in range(len(board[0]))]
    # loop through the board and append all items with same index number to the appropriate columns list
    for row in board:
        for index, item in enumerate(row):
            columns[index].append(item)
    # return the transposed board
    return columns


def check_verticals(board):
    """function takes in as parameter the current board and checks to see if there are any wins
    on the board in the vertical columns.. return if 1 wins, 2 wins, or no win occurs.."""
    # call transposed function to tranpose board in order to iterate through rows and check for wins
    transposed_board = transpose(board)
    # iterate through each row in the board and check for wins
    # initiate column counter so we know which column winner is in
    column = 1
    rownums = []  # initiate empty row numbers list
    for row in transposed_board:
        # set conditional for first possible win for 1
        if row[:4] == [1, 1, 1, 1]:
            winner = 1  # set winner to 1
            row_nums = [1, 2, 3, 4]  # id row nums of the winner
            break  # if conditional executes then program breaks out of conditional and returns proper values
        elif row[1:5] == [1, 1, 1, 1]:  # second possible win
            winner = 1
            row_nums = [2, 3, 4, 5]
            break
        elif row[2:] == [1, 1, 1, 1]:  # third possible win
            winner = 1
            row_nums = [3, 4, 5, 6]
            break
        # repeat same process but for if 2 is the winner (same logic)
        elif row[:4] == [2, 2, 2, 2]:  # first possible win for 2
            winner = 2  # set winner to 2
            row_nums = [1, 2, 3, 4]  # id row nums of the winner
            break
        elif row[1:5] == [2, 2, 2, 2]:  # second possible win for 2
            winner = 2
            row_nums = [2, 3, 4, 5]
            break
        elif row[2:] == [2, 2, 2, 2]:  # third possible win for 2
            winner = 2
            row_nums = [3, 4, 5, 6]
            break
        else:  # if no winner then winner is assigned 0 and is returned indicating no winner
            winner = 0
            row_nums = []

        column += 1  # increment column counter so proper column number of winner can be identified
        # if there is no winner, then only return winner = 0
        if winner == 0:
            column = 0
            return winner
    # if there is a winner, return the winner, column, and the row nums so winner can be identified on the board
    return winner, column, row_nums


def check_diagonals(board):
    """function takes in board as a parameter and checks to see if there is a diagonal winner"""
    # convert inputted board into a numpy array with data type string
    board = np.array(board, dtype=str)

    # -create first 6 diagonals from board by using numpy diagonal function with the diagonal number as second argunment
    # -convert each diagonal array back into a list
    # -convert list into a string so we can use the find() function to see if there is a winner
    diag_1 = "".join(list(np.diag(board, k=3)))
    diag_2 = "".join(list(np.diag(board, k=2)))
    diag_3 = "".join(list(np.diag(board, k=1)))
    diag_4 = "".join(list(np.diag(board, k=0)))
    diag_5 = "".join(list(np.diag(board, k=-1)))
    diag_6 = "".join(list(np.diag(board, k=-2)))

    # flip the board using numpy flip function so function can get the other 6 diagonals
    # repeat the same process used above in the other 6 diagonals
    flipped_board = np.flipud(board)
    diag_7 = "".join(list(np.diag(flipped_board, k=3)))
    diag_8 = "".join(list(np.diag(flipped_board, k=2)))
    diag_9 = "".join(list(np.diag(flipped_board, k=1)))
    diag_10 = "".join(list(np.diag(flipped_board, k=0)))
    diag_11 = "".join(list(np.diag(flipped_board, k=-1)))
    diag_12 = "".join(list(np.diag(flipped_board, k=-2)))

    # create a list of the diagonals (list of strings)
    list_of_diags = [
        diag_1,
        diag_2,
        diag_3,
        diag_4,
        diag_5,
        diag_6,
        diag_7,
        diag_8,
        diag_9,
        diag_10,
        diag_11,
        diag_12,
    ]

    # initiate counter before looping through the diagonals list so we can return the diagonal number of the winner
    counter = 0
    # have winner initially set as 0 before the loop so if no winner is found it can be returned later
    winner = 0
    # initiate for loop to iterate through the diagonals list
    for diag in list_of_diags:
        # increment counter variable for the diagonals
        counter += 1
        # create finder variables (1/2) that will use the find() function to locate a winner
        find_winner_1 = diag.find("1111")  # will find winner for 1
        find_winner_2 = diag.find("2222")  # will find winner for two
        # -finder returns index value where string is found, but returns -1 if string isnt found
        # -if winner variable != -1, there is a winner because it is assigned to an index number
        if find_winner_1 != -1:
            # assign winner as 1 and return
            winner = 1
            return winner, counter, find_winner_1
        # process is repeated for player 2
        if find_winner_2 != -1:
            winner = 2
            return winner, counter, find_winner_2

    # if winning move was not found in the board for any diagonal, return that there was no diagonal winner
    if winner != 1 and winner != 2:
        no_winner = 0
        return no_winner


def check_win(board):
    return check_diagonals(board) or check_horizontals(board) or check_verticals(board)


empty_board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def flip(board):
    return [row[::-1] for row in board]


def copy_board(board):
    result = []
    for row in board:
        result.append(row[:])

    return result


def drop_piece(player, column, board):
    columns = transpose(board)
    flipped = flip(columns)
    board = copy_board(board)

    for dex, cell in enumerate(flipped[column]):
        if cell == 0:
            flipped[column][dex] = player
            break
    return transpose(flip(flipped))
