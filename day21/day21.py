from functools import cache
from typing import Tuple, List

from aocd.models import Puzzle

from day17.day17 import in_bounds

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


@cache
def simulate_from_point(sy, sx, board, max_steps, print_result=False):
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
    if print_result:
        print_board(list(queue), board)
    return len(queue)


def part1(input_data, max_steps, debug=False):
    board = parse(input_data)
    sy, sx = start_pos(board)
    return simulate_from_point(sy, sx, board, max_steps, print_result=debug)


def get_infinite_board(y, x, board):
    if not in_bounds(board, y, x):
        pass
    return board[y % len(board)][x % len(board[0])]


def print_board(queue: List[Tuple[int, int]], board):
    new_board = []
    for row in board:
        new_row = []
        for cell in row:
            new_row.append(cell)
        new_board.append(new_row)

    for y, x in queue:
        new_board[y][x] = 'O'

    for row in new_board:
        print(''.join(row))


def part2_naive(input_data, max_steps):
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
    print(len(queue))
    return len(queue)


def part2(input_data, steps):
    board = parse(input_data)
    size = len(board)
    n = (steps - size // 2) // size
    top_mid = simulate_from_point(size - 1, size // 2, board, size - 1)
    left_mid = simulate_from_point(size // 2, size - 1, board, size - 1)
    right_mid = simulate_from_point(size // 2, 0, board, size - 1)
    bottom_mid = simulate_from_point(0, size // 2, board, size - 1)

    top_left_small = simulate_from_point(size - 1, size - 1, board, size // 2 - 1)
    top_left_big = simulate_from_point(size - 1, size - 1, board, size // 2 + size - 1)

    top_right_small = simulate_from_point(size - 1, 0, board, size // 2 - 1)
    top_right_big = simulate_from_point(size - 1, 0, board, size // 2 + size - 1)

    bottom_left_small = simulate_from_point(0, size - 1, board, size // 2 - 1)
    bottom_left_big = simulate_from_point(0, size - 1, board, size // 2 + size - 1)

    bottom_right_small = simulate_from_point(0, 0, board, size // 2 - 1)
    bottom_right_big = simulate_from_point(0, 0, board, size // 2 + size - 1)

    start = simulate_from_point(size // 2, size // 2, board, size // 2 + size)
    nonstart = simulate_from_point(size // 2, size // 2, board, size // 2 + size + 1)

    result = top_mid + left_mid + bottom_mid + right_mid

    even = n ** 2
    odd = (n - 1) ** 2
    result += even * start
    result += odd * nonstart

    result += n * top_left_small
    result += (n - 1) * top_left_big

    result += n * top_right_small
    result += (n - 1) * top_right_big

    result += n * bottom_left_small
    result += (n - 1) * bottom_left_big

    result += n * bottom_right_small
    result += (n - 1) * bottom_right_big

    return result


def main():
    assert 16 == part1(puzzle.examples[0].input_data, 6, debug=True)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data, 64)
    print("part1 OK")

    assert 16 == part2_naive(puzzle.examples[0].input_data, 6)
    print("part2 example 6 OK")
    assert 50 == part2_naive(puzzle.examples[0].input_data, 10)
    print("part2 example 10 OK")
    assert 1594 == part2_naive(puzzle.examples[0].input_data, 50)
    print("part2 example 50 OK")
    assert 3687 == part2_naive(puzzle.examples[0].input_data, 75)
    print("part2 example 75 OK")
    assert 6536 == part2_naive(puzzle.examples[0].input_data, 100)
    print("part2 example 100 OK")
    assert 167004 == part2_naive(puzzle.examples[0].input_data, 500)
    print("part2 example 500 OK")

    print("Naive part2 solution for next examples is too slow")

    n = 1
    steps = n * 131 + 65
    assert part2_naive(puzzle.input_data, steps) == part2(puzzle.input_data, steps)
    print("Example with n=1 OK")

    n = 2
    steps = n * 131 + 65
    assert part2_naive(puzzle.input_data, steps) == part2(puzzle.input_data, steps)
    print("Example with n=2 OK")

    puzzle.answer_b = part2(puzzle.input_data, 26501365)
    print("part2 OK")


if __name__ == '__main__':
    main()
