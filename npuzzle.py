from typing import List
from math import sqrt, floor
from collections import namedtuple, deque
from minpq import MinPQ

Move = namedtuple("Move", ["board"])

def get_neighbors(move: Move) -> List[Move]:
    arr: List[int] = list(move.board)
    n = floor(sqrt(len(arr)))
    empty_position = arr.index(0)
    empty_row, empty_col = divmod(empty_position, n)
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = empty_row + dr, empty_col + dc
        if 0 <= new_row < n and 0 <= new_col < n:
            new_pos = new_row * n + new_col
            arr[empty_position], arr[new_pos] = arr[new_pos], arr[empty_position] # make the move
            neighbors.append(Move(tuple(arr)))
            arr[new_pos], arr[empty_position] = arr[empty_position], arr[new_pos] # undo the move
    return neighbors

def hamming(move: Move):
    distance = 0
    for (i, k) in enumerate(move.board, start=1):
        if k != 0 and k != i:
            distance += 1
    return distance

def manhattan(move: Move):
    n = floor(sqrt(len(move.board)))
    distance, row, col = 0, 0, 0
    for (i, k) in enumerate(move.board, start=1):
        if k != 0 and k != i:
            col = abs((i-1) % n - (k-1) % n)
            row = abs((i-1) // n - (k-1) // n)
            distance += (col + row)
    return distance

def is_goal(move: Move)-> bool:
        for (i, k) in  enumerate(move.board[:-1], start=1):
            if i != k:
                return False
        return True

def generate_solution(parent: map, move: Move) -> List[Move]:
    p = parent[move]
    moves: List[Move] = [move] 
    while p is not None:
        moves.append(p)
        p = parent.get(p)
    return list(reversed(moves))

def solve(initial: Move) -> List[Move]:
    q = deque()
    q.append(initial)
    visited, parent = {}, {}
    while len(q) != 0:
        current_move = q.popleft()
        if is_goal(current_move):
            return generate_solution(parent, current_move)
        neighbors: List[Move] = get_neighbors(current_move)

        for n in neighbors:
            if visited.get(n) is None:
                q.append(n)
                parent[n] = current_move

        visited[current_move] = True
    
    return None


def solve_using_minpq(initial: Move, comparator = lambda m1, m2 : hamming(m1)-hamming(m2)) -> List[Move]:
    pq: MinPQ = MinPQ(comparator)
    pq.insert(initial)
    visited, parent = {}, {}
    while pq.isempty() is False:
        current_move = pq.delmin()
        if is_goal(current_move):
            return generate_solution(parent, current_move)
        neighbors: List[Move] = get_neighbors(current_move)

        for n in neighbors:
            if visited.get(n) is None:
                pq.insert(n)
                parent[n] = current_move

        visited[current_move] = True
    
    return None


def main(tiles: List[int]):
    # solving using simple queue
    q_steps: List[Move] = solve(Move(tuple(tiles)))
    if q_steps is not None:
        print(f"solution  with simple queue: {len(q_steps)}")
    
    # solving using minimum prority queue using hamming distance as comparator
    hamming_pq_steps: List[Move] = solve_using_minpq(Move(tuple(tiles)))
    if hamming_pq_steps is not None:
        print(f"solution  with priority queue: {len(hamming_pq_steps)}")
        for st in hamming_pq_steps:
            print(st)

    # solving using minimum prority queue using manhattan distance as comparator
    manhattan_pq_steps: List[Move] = solve_using_minpq(Move(tuple(tiles)), comparator=lambda m1, m2: manhattan(m1)-manhattan(m2))
    if manhattan_pq_steps is not None:
        print(f"solution  with priority queue: {len(manhattan_pq_steps)}")
        for st in manhattan_pq_steps:
            print(st)

if __name__ == '__main__':

    n_puzzle_size = input("Enter the size of the NPuzzle.\n").strip()
    n_puzzle_size = int(n_puzzle_size)
    
    row_suffix = {1: "first", 2: "second", 3: "third"}
    k = 0
    tiles = []
    
    while k < n_puzzle_size:
        if k <= 3:
            row_txt = input(f"Enter the {row_suffix[k+1]} row of numbers.\n")
        else:
            row_txt = input(f"Enter the {k+1}'th row of numbers.\n")
        tiles.extend([int(a.strip()) for a in row_txt.split()])
        k += 1

    main(tiles)




