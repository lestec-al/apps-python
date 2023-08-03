import random, copy, time

def print_board(board):
    """Print board on the command line"""
    print("")
    for i in board[0:3]:
        print(f"{i[0:3]} {i[3:6]} {i[6:]}")
    print("-----------------------------")
    for i in board[3:6]:
        print(f"{i[0:3]} {i[3:6]} {i[6:]}")
    print("-----------------------------")
    for i in board[6:]:
        print(f"{i[0:3]} {i[3:6]} {i[6:]}")
    print("")

def solver(board):
    """Sudoku solver
    board: ready sudoku board"""
    print("\nBefore:")
    print_board(board)
    start = time.time()
    tries = 0
    board1 = copy.deepcopy(board)
    while True:
        board = copy.deepcopy(board1)
        i_row = -1
        for row in board:
            i_row += 1
            i_item = -1
            for item in row:
                i_item += 1
                if item == 0:# board[i_row][i_item]
                    while_counter = 0
                    ready = False
                    while ready == False and while_counter < 100:
                        while_counter += 1
                        random_int = random.randint(1,9)
                        # Checking columns
                        check_column = True
                        for i in range(1,12):
                            if i_row - i >= 0:
                                if board[i_row - i][i_item] == random_int:
                                    check_column = False
                            if i_row + i <= 8:
                                if board[i_row + i][i_item] == random_int:
                                    check_column = False
                        # Checking squares
                        check_squares = True
                        if (i_row == 0 or i_row == 3 or i_row == 6) and (i_item == 0 or i_item == 3 or i_item == 6):# Left up square
                            if (
                            (board[i_row][i_item + 1] == random_int) or (board[i_row][i_item + 2] == random_int) or
                            (board[i_row + 1][i_item] == random_int) or (board[i_row + 1][i_item + 1] == random_int) or (board[i_row + 1][i_item + 2] == random_int) or
                            (board[i_row + 2][i_item] == random_int) or (board[i_row + 2][i_item + 1] == random_int) or (board[i_row + 2][i_item + 2] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 0 or i_row == 3 or i_row == 6) and (i_item == 1 or i_item == 4 or i_item == 7):# Middle up
                            if (
                            (board[i_row][i_item - 1] == random_int) or (board[i_row][i_item + 1] == random_int) or
                            (board[i_row + 1][i_item - 1] == random_int) or (board[i_row + 1][i_item] == random_int) or (board[i_row + 1][i_item + 1] == random_int) or
                            (board[i_row + 2][i_item - 1] == random_int) or (board[i_row + 2][i_item] == random_int) or (board[i_row + 2][i_item + 1] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 0 or i_row == 3 or i_row == 6) and (i_item == 2 or i_item == 5 or i_item == 8):# Right up
                            if (
                            (board[i_row][i_item - 2] == random_int) or (board[i_row][i_item - 1] == random_int) or
                            (board[i_row + 1][i_item - 2] == random_int) or (board[i_row + 1][i_item - 1] == random_int) or (board[i_row + 1][i_item] == random_int) or
                            (board[i_row + 2][i_item - 2] == random_int) or (board[i_row + 2][i_item - 1] == random_int) or (board[i_row + 2][i_item] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 1 or i_row == 4 or i_row == 7) and (i_item == 0 or i_item == 3 or i_item == 6):# left
                            if (
                            (board[i_row - 1][i_item] == random_int) or (board[i_row - 1][i_item + 1] == random_int) or (board[i_row - 1][i_item + 2] == random_int) or
                            (board[i_row][i_item + 1] == random_int) or (board[i_row][i_item + 2] == random_int) or
                            (board[i_row + 1][i_item] == random_int) or (board[i_row + 1][i_item + 1] == random_int) or (board[i_row + 1][i_item + 2] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 1 or i_row == 4 or i_row == 7) and (i_item == 1 or i_item == 4 or i_item == 7):# Middle
                            if (
                            (board[i_row - 1][i_item - 1] == random_int) or (board[i_row - 1][i_item] == random_int) or (board[i_row - 1][i_item + 1] == random_int) or
                            (board[i_row][i_item - 1] == random_int) or (board[i_row][i_item + 1] == random_int) or
                            (board[i_row + 1][i_item - 1] == random_int) or (board[i_row + 1][i_item] == random_int) or (board[i_row + 1][i_item + 1] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 1 or i_row == 4 or i_row == 7) and (i_item == 2 or i_item == 5 or i_item == 8):# Right
                            if (
                            (board[i_row - 1][i_item - 2] == random_int) or (board[i_row - 1][i_item - 1] == random_int) or (board[i_row - 1][i_item] == random_int) or
                            (board[i_row][i_item - 2] == random_int) or (board[i_row][i_item - 1] == random_int) or
                            (board[i_row + 1][i_item - 2] == random_int) or (board[i_row + 1][i_item - 1] == random_int) or (board[i_row + 1][i_item] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 2 or i_row == 5 or i_row == 8) and (i_item == 0 or i_item == 3 or i_item == 6):# left down
                            if (
                            (board[i_row - 2][i_item] == random_int) or (board[i_row - 2][i_item + 1] == random_int) or (board[i_row - 2][i_item + 2] == random_int) or
                            (board[i_row - 1][i_item] == random_int) or (board[i_row - 1][i_item + 1] == random_int) or (board[i_row - 1][i_item + 2] == random_int) or
                            (board[i_row][i_item + 1] == random_int) or (board[i_row][i_item + 2] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 2 or i_row == 5 or i_row == 8) and (i_item == 1 or i_item == 4 or i_item == 7):# Middle down
                            if (
                            (board[i_row - 2][i_item - 1] == random_int) or (board[i_row - 2][i_item] == random_int) or (board[i_row - 2][i_item + 1] == random_int) or
                            (board[i_row - 1][i_item - 1] == random_int) or (board[i_row - 1][i_item] == random_int) or (board[i_row - 1][i_item + 1] == random_int) or
                            (board[i_row][i_item - 1] == random_int) or (board[i_row][i_item + 1] == random_int)
                            ):
                                check_squares = False
                        if (i_row == 2 or i_row == 5 or i_row == 8) and (i_item == 2 or i_item == 5 or i_item == 8):# Right down
                            if (
                            (board[i_row - 2][i_item - 2] == random_int) or (board[i_row - 2][i_item - 1] == random_int) or (board[i_row - 2][i_item] == random_int) or
                            (board[i_row - 1][i_item - 2] == random_int) or (board[i_row - 1][i_item - 1] == random_int) or (board[i_row - 1][i_item] == random_int) or
                            (board[i_row][i_item - 2] == random_int) or (board[i_row][i_item - 1] == random_int)
                            ):
                                check_squares = False
                        # Checking number
                        if (random_int not in board[i_row]) and (check_column == True) and (check_squares == True):
                            board[i_row][i_item] = random_int
                            ready = True
        # Checking result
        zero_count = 0
        for row in board:
            for item in row:
                if item == 0:
                    zero_count += 1
        if zero_count == 0:
            print(f"Solved in {int((time.time()-start)/60) if (time.time()-start)/60 > 1 else int(time.time()-start)}\n")
            print("After:")
            print_board(board)
            return board
        else:
            tries += 1
        # If too many tries - not solved
        if tries >= 10000:
            print(f"Not solved in {int((time.time()-start)/60) if (time.time()-start)/60 > 1 else int(time.time()-start)}\n")
            return board

if __name__ == "__main__":
    # Board for solving
    board = [
        [4, 0, 0, 0, 3, 2, 0, 0, 5],
        [5, 0, 8, 7, 6, 4, 2, 1, 0],
        [0, 0, 2, 5, 9, 0, 7, 0, 4],
        [3, 0, 5, 8, 0, 1, 0, 0, 6],
        [0, 2, 6, 0, 4, 9, 0, 5, 0],
        [8, 0, 1, 0, 0, 0, 4, 0, 0],
        [9, 0, 3, 0, 0, 7, 5, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 4, 6, 8, 0, 0, 0, 0]]

    # Solver itself
    solver(board)