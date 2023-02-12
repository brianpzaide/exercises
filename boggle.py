"TODO implement trie datastructure"
from m_trie import *

def getOptions(board, r, c):
    options = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c+1), (r+1, c+1), (r+1, c), (r+1, c-1), (r, c-1)]
    n_r = len(board)
    n_c = len(board[0])
    options_filtered = [(row, col) for row, col in options if row in range(n_r) and col in range(n_c) and not board[row][col]["taken"]]
    return options_filtered



def solve(board):
    def solve_recursive(board, row, col, current_word):
        global m_trie
        nonlocal found_words
        options = getOptions(board, row, col)
        for r, c in options:
            current_word = current_word + board[r][c]["ch"]
            board[r][c]["taken"] = True
            if m_trie.search(current_word, startswith=True):
                if m_trie.search(current_word, startswith=False):
                    found_words.add(current_word)
                solve_recursive(board, r, c, current_word)
            board[r][c]["taken"] = False
            current_word = current_word[:len(current_word)-1]

    n_r = len(board)
    n_c = len(board[0])
    found_words = set()
    for r in range(n_r):
        for c in range(n_c):
            board[r][c]["taken"] = True
            solve_recursive(board, r, c, board[r][c]["ch"])
            board[r][c]["taken"] = False
    return found_words

def initialize_board(alphabets, rows, cols):
    board = []
    i = 0
    for r in range(rows):
        board.append([{"ch": alphabets[c+i], "taken": False} for c in range(cols)])
        i += cols

    return board

def print_puzzle(board):
    for row in range(len(board)):
        print(board[row][:])

def main():

    global m_trie

    m_trie = M_Trie()
    words = m_trie.getAllwords()
    print("length of word_list in m_trie: {}".format(len(words)))
    
    print("enter board size: ")
    n_rows = int(input("no of rows: "))
    n_cols = int(input("no of columns: "))
    print("enter board letters separated by space: ")
    alphabets = input().split(" ")

    board = initialize_board(alphabets, n_rows, n_cols)
    print_puzzle(board)
    print("solving...")
    found_words = solve(board)
    print("solved Hurray!")
    print(found_words)
    print(found_words.isdisjoint(set(['LION','KING','PEAR','BEAR'])))
    

if __name__ == "__main__":
    main()