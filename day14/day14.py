from enum import Enum

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=14)


def parse(input_data):
    return [list(row) for row in input_data.split("\n")]


def find_empty(data, y, x):
    empty = y
    for fall_y in reversed(range(0, y)):
        if data[fall_y][x] == '.':
            empty = fall_y
        else:
            break
    return empty


def calc_load(data):
    load = 0
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == 'O':
                load += len(data) - y
    return load


def fall_rocks(data):
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == 'O':
                stop_y = find_empty(data, y, x)
                if stop_y != y:
                    data[y][x] = '.'
                    data[stop_y][x] = 'O'
    return data


# Example result
# OOOO.#.O..
# OO..#....#
# OO..O##..O
# O..#.OO...
# ........#.
# ..#....#.#
# ..O..#.O.O
# ..O.......
# #....###..
# #....#....

def part1(input_data):
    data = parse(input_data)
    after_fall = fall_rocks(data)
    return calc_load(after_fall)


class Directions(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


def rotate_board_right(board):
    new_board = []
    for x in range(len(board[0])):
        new_row = []
        for y in reversed(range(len(board))):
            new_row.append(board[y][x])
        new_board.append(new_row)
    return new_board


def fall_rocks_in_direction(board, direction):
    rotations = {
        Directions.NORTH: 0,
        Directions.WEST: 1,
        Directions.EAST: 3,
        Directions.SOUTH: 2,
    }.get(direction)
    rotated = board.copy()
    for _ in range(rotations):
        rotated = rotate_board_right(rotated)
    rotated = fall_rocks(rotated)
    if rotations != 0:
        for _ in range(4 - rotations):
            rotated = rotate_board_right(rotated)
    return rotated


def board_to_str(board):
    return '\n'.join([''.join(row) for row in board])


def print_board(board):
    print(board_to_str(board))
    print()


CYCLES = 1000000000

cycle_cache = {}


def find_naive_cycle(seq):
    if len(seq) < 1000:  # wait for at least 1000 values
        return None
    for cycle_len in range(6, len(seq) - 6):
        if seq[-cycle_len:] == seq[-cycle_len - cycle_len: - cycle_len]:
            return cycle_len
    return None


def find_subarray_cycle(seq):
    for cycle_len in range(6, len(seq) - 6):
        if seq[-cycle_len:] == seq[-cycle_len - cycle_len: - cycle_len]:
            return cycle_len
    return None


def find_hash_cycle(seq):
    for cycle_len in range(6, len(seq) - 6):
        cycle_hash = hash(tuple(seq[-cycle_len:]))
        if cycle_hash in cycle_cache:
            prev_len = cycle_cache[cycle_hash]
            cycle_cache.clear()
            return len(seq) - prev_len
        else:
            cycle_cache[cycle_hash] = len(seq)
    return None


def tortoise_and_hare(seq):
    if len(seq) <= 6:
        return None
    tortoise = len(seq) - 1
    hare = len(seq) - 2
    cycle_len = 1
    while seq[tortoise] != seq[hare] or cycle_len <= 6:
        tortoise -= 1
        hare -= 2
        cycle_len += 1
        if hare < 0:
            return None
    return cycle_len


def part2(input_data, cycle_det_func):
    board = parse(input_data)
    directions = [Directions.NORTH, Directions.WEST, Directions.SOUTH, Directions.EAST]
    after_cycle_load = []
    cycle_len = None
    for cycle_len in range(CYCLES):
        for direction in directions:
            after_fall = fall_rocks_in_direction(board, direction)
            board = after_fall
        after_cycle_load.append(calc_load(board))
        cycle_len = cycle_det_func(after_cycle_load)
        if cycle_len is not None:
            break
    print("cycle length", cycle_len)
    cycle_start = len(after_cycle_load) - cycle_len
    reminder = (CYCLES - cycle_start) % cycle_len
    load = after_cycle_load[cycle_start + reminder - 1]
    return load


def main():
    assert find_empty([['.'], ['.'], ['O']], 2, 0) == 0
    assert find_empty([['#'], ['.'], ['O']], 2, 0) == 1
    assert find_empty([['#'], ['O'], ['O']], 2, 0) == 2
    assert find_empty([['O'], ['.'], ['.']], 0, 0) == 0
    assert calc_load([['.', '#'], ['#', 'O'], ['O', '.']]) == 3
    assert 136 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert rotate_board_right([['O'], ['.'], ['.']]) == [['.', '.', 'O']]
    assert fall_rocks_in_direction([['.', '.', 'O']], Directions.WEST) == [['O', '.', '.']]
    cycle_detection_algorith = tortoise_and_hare
    assert 64 == part2(puzzle.examples[0].input_data, cycle_detection_algorith)
    print("part2 example OK")
    import time

    start_time = time.time()
    puzzle.answer_b = part2(puzzle.input_data, cycle_detection_algorith)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    print("part2 OK")


if __name__ == '__main__':
    main()

# init with 1000 cycles    - 5.44 s
# subarray cycle detection - 0.96 s
# tortoise and hare        - 0.96 s
# hash cycle detection     - 0.84 s
