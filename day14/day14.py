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
    correct_rotation = rotated
    if rotations != 0:
        for _ in range(4 - rotations):
            rotated = rotate_board_right(rotated)
    return rotated


def board_to_str(board):
    return '\n'.join([''.join(row) for row in board])


def print_board(board):
    print(board_to_str(board))
    print()


# CYCLES = 4
CYCLES = 1000000000
INIT_CYCLES = 1000


def part2(input_data):
    board = parse(input_data)
    directions = [Directions.NORTH, Directions.WEST, Directions.SOUTH, Directions.EAST]
    after_cycle_load = []
    for cycle in range(CYCLES):
        for direction in directions:
            after_fall = fall_rocks_in_direction(board, direction)
            board = after_fall
        after_cycle_load.append(calc_load(board))
        if len(after_cycle_load) > INIT_CYCLES:
            break
    for cycle_len in range(1, INIT_CYCLES):
        if after_cycle_load[-cycle_len:] == after_cycle_load[-cycle_len - cycle_len: - cycle_len]:
            cycle_start = len(after_cycle_load) - cycle_len
            reminder = (CYCLES - cycle_start) % cycle_len
            load = after_cycle_load[cycle_start + reminder - 1]
            return load
    raise RuntimeError("no cycle found")


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
    assert 64 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
