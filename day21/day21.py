from collections import deque, defaultdict
from functools import cache
from re import findall

from tqdm import tqdm

from day17.day17 import in_bounds
from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=21)


def parse(input_data):
    return tuple(tuple(row) for row in input_data.split("\n"))


def start_pos(board):
    for y, row in enumerate(board):
        for x, c in enumerate(row):
            if c == 'S':
                return y, x
    return None


neighbours = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
]


def simulate_from_point(sy, sx, board, max_steps):
    queue = {(sy, sx)}
    next_queue = set()
    for i in range(max_steps):
        for y, x in queue:
            for dy, dx in neighbours:
                ny, nx = y + dy, x + dx
                if in_bounds(board, ny, nx) and board[ny][nx] != '#':
                    next_queue.add((ny, nx))
        queue = next_queue
        next_queue = set()
    return len(queue)


def part1(input_data, max_steps):
    board = parse(input_data)
    sy, sx = start_pos(board)
    return simulate_from_point(sy, sx, board, max_steps)


def get_infinite_board(y, x, board):
    if not in_bounds(board, y, x):
        pass
    return board[y % len(board)][x % len(board[0])]


def print_board(queue, board):
    new_board = []
    for i in range(3):
        for row in board:
            new_row = []
            for i in range(3):
                for cell in row:
                    new_row.append(cell)
            new_board.append(new_row)

    for (y, x) in queue:
        new_board[y + len(board)][x + len(board[0])] = 'O'

    for row in new_board:
        print(''.join(row))


def part2(input_data, max_steps):
    board = parse(input_data)
    sy, sx = start_pos(board)
    queue = {(sy, sx)}
    next_queue = set()

    for i in range(max_steps):
        for y, x in queue:
            for dy, dx in neighbours:
                ny, nx = y + dy, x + dx
                if get_infinite_board(ny, nx, board) != '#':
                    next_queue.add((ny, nx))
        queue = next_queue
        next_queue = set()
    # print_board(queue, board)
    return len(queue)


def main():
    assert 16 == part1(puzzle.examples[0].input_data, 6)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data, 64)
    print("part1 OK")

    assert 16 == part2(puzzle.examples[0].input_data, 6)
    print("part2 example 6 OK")
    assert 50 == part2(puzzle.examples[0].input_data, 10)
    print("part2 example 10 OK")
    assert 1594 == part2(puzzle.examples[0].input_data, 50)
    print("part2 example 50 OK")
    assert 3687 == part2(puzzle.examples[0].input_data, 75)
    print("part2 example 75 OK")
    assert 6536 == part2(puzzle.examples[0].input_data, 100)
    print("part2 example 100 OK")
    assert 167004 == part2(puzzle.examples[0].input_data, 500)
    print("part2 example 500 OK")

    print("Part2 solution for next examples is too slow")
    return

    assert 668697 == part2(puzzle.examples[0].input_data, 1000)
    print("part2 example 1000 OK")
    assert 16733044 == part2(puzzle.examples[0].input_data, 5000)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data, 26501365)
    print("part2 OK")


if __name__ == '__main__':
    main()
