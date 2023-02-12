
def getOptions(puzzle, row, col):
    all_options= set([1,2,3,4,5,6,7,8,9])
    start_rc = [[(0,0),(0,3),(0,6)], [(3,0), (3,3), (3,6)], [(6,0), (6,3), (6,6)]]
    exclusions = set()
    for r in range(9):
        temp = puzzle[r][col]
        if temp != 0:
            exclusions.add(temp)
    for c in range(9):
        temp = puzzle[row][c]
        if temp != 0: exclusions.add(temp)
        start_r, start_c = start_rc[row//3][col//3]
    for r in range(3):
        for c in range(3):
            temp = puzzle[start_r + r][start_c+c]
            if temp != 0: exclusions.add(temp)
    
    return all_options-exclusions


def solve(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                options = getOptions(puzzle, row, col)
                for opt in options:
                    puzzle[row][col] = opt
                    if solve(puzzle):
                        return True
                    else:
                        puzzle[row][col] = 0
                return False
    return True

def print_puzzle(puzzle):
    for row in range(9):
        print(puzzle[row][:])

def main():
    puzzle = []
    puzzle_lines = (input()).split(" ")
    print(puzzle_lines)
    for line in puzzle_lines:
        puzzle.append([int(num) for num in line.split(",")])
    print_puzzle(puzzle)
    print("solving")
    solve(puzzle)
    print_puzzle(puzzle)

if __name__ == "__main__":
    main()