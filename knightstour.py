def check_board_filled(board):
    n_r = len(board)
    n_c = len(board[0])
    total = 0
    for r in range(n_r):
        total += sum(board[r])
    return True if total == n_r*n_c else False

def getOptions(board, r, c):
    moves = [(r-2, c+1), (r-1, c+2), (r+1, c+2), (r+2, c+1), (r+2, c-1), (r+1, c-2), (r-1, c-2), (r-2, c-1)]
    n_r = len(board)
    n_c = len(board[0])
    options = [(row, col) for row, col in moves if row in range(n_r) and col in range(n_c)]
    return options


def solve(board, row, col, path):
    if check_board_filled(board): 
        return True
    options = getOptions(board, row, col)
    for r, c in options:
        if board[r][c] == 0:
            board[r][c] = 1
            path.append((r,c))
            if solve(board, r, c, path):
                return True
            else:
                board[r][c] = 0
                path.pop(len(path)-1)
    return False

def initialize_board(rows, cols):
    board = []
    for r in range(rows):
        board.append([0 for c in range(cols)])
    return board

def print_puzzle(board):
    for row in range(len(board)):
        print(board[row][:])

def update_board(board, path):
    n = 2
    for r, c in path:
        board[r][c] = n
        n += 1

def main():
    
    print("enter board size: ")
    n_rows = int(input())
    n_cols = int(input())
    board = initialize_board(n_rows, n_cols)
    board[0][0] = 1
    path = []
    print_puzzle(board)
    print("solving...")
    if solve(board,0,0, path):
        print("solved Hurray!")
        update_board(board, path)
        print_puzzle(board)
    else:
        print("can not be solved")

if __name__ == "__main__":
    main()