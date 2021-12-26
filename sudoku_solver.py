import random
import math

def solve_sudoku(grid, row, col):
    if (row == 8 and col == 9):
        return True
    if col == 9:
        row += 1
        col = 0
    if grid[row][col] != "0":
        return solve_sudoku(grid, row, col + 1)

    for num in range(1, 10, 1):
        if valid(grid, num, (row,col)):
            grid[row][col] = num
            if solve_sudoku(grid, row, col +1):
                return True
        grid[row][col] = 0
    return False


def can_solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    else: 
        row, col = empty 

    for i in range (1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if can_solve(board):
                return True
            board[row][col] = 0
    return False


def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == str(num) and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == str(num) and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == str(num) and (i,j) != pos:
                return False

    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i !=0:
            print("- - -   - - -    - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def get_board(filename, start):
    file = open(filename, "r")
    lines = file.readlines()
    grid = []
    for i in range(0,9):
        line = lines[start+i]
        line = line.strip()
        row = line.split(" ")
        grid.append(row)
    file.close()
    return grid


def get_rand_board(filename):
    num_lines = sum(1 for line in open('input.in'))
    rand = random.randint(0, num_lines)
    print(num_lines)
    print(rand)
    if rand == num_lines:
        rounded = num_lines - 9
    else:
        rounded = (rand//10)*10
        print("ROUNDED " + str(rounded))
    return get_board("input.in", rounded)
