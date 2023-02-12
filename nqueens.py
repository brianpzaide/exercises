def check_diag(board, row, col, anti=False):
    height = len(board)
    width = len(board[0])
    diag_elems = []
    if anti:
        # print("anti row: {}, col: {}: ".format(row, col))
        upper = list(zip(range(row, -1, -1), range(col, -1, -1)))
        # print("upper: ", upper)
        lower = list(zip(range(row+1, height), range(col+1, width)))
        # print("lower: ", lower)
        l = upper + lower
        diag_elems = [board[r][c] for r, c in l]
    else:
        # print("main row: {}, col: {}: ".format(row, col))
        upper = list(zip(range(row, -1, -1), range(col, width)))
        # print("upper: ", upper)
        lower = list(zip(range(row+1, height), range(col-1, -1, -1)))
        # print("lower: ", lower)
        l = upper + lower
        
        diag_elems = [board[r][c] for r, c in l]

    return sum(diag_elems) == 0



def getOptions(board, col):
    options = []
    n_r = len(board)
    n_c = len(board[0])
    for r in range(n_r):
        if sum(board[r][:]) == 0 and check_diag(board, r, col) and check_diag(board, r, col, anti=True):
            options.append(r)
    return options


def solve(board, col):
    if col == len(board[0]): return True
    options = getOptions(board, col)
    # print("row: {}, col: {}, options: {}".format(row, col, options))
    for row in options:
        board[row][col] = 1
        # print("row: {}, col: {}".format(row, col))
        # print_puzzle(puzzle)
        if solve(board, col+1):
            return True
        else:
            board[row][col] = 0
    return False

def initialize_board(rows, cols):
    board = []
    for r in range(rows):
        board.append([0 for c in range(cols)])
    return board

def print_puzzle(board):
    for row in range(len(board)):
        print(board[row][:])

def main():
    
    print("enter board size: ")
    n_rows = int(input())
    n_cols = int(input())
    print("solving")
    board = initialize_board(n_rows, n_cols)
    print_puzzle(board)
    print("solving...")
    if solve(board, 0):
        print("solved Hurray!")
        print_puzzle(board)
    else:
        print("can not be solved")

if __name__ == "__main__":
    main()