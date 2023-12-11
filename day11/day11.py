from itertools import count, product
from re import findall

from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=11)


def parse(input_data):
    data = input_data.split("\n")
    empty_rows = []
    positions = []
    for y, line in enumerate(data):
        empty = True
        for x, char in enumerate(line):
            if char == '#':
                positions.append((y, x))
                empty = False
        if empty:
            empty_rows.append(y)
    empty_cols = []
    for x, _ in enumerate(data[0]):
        empty = True
        for y in range(len(data)):
            if data[y][x] == '#':
                empty = False
                break
        if empty:
            empty_cols.append(x)
    return positions, empty_cols, empty_rows


def solve(input_data, empty_space_size):
    positions, empty_cols, empty_rows = parse(input_data)
    all_distances = [[float('inf') for _ in positions] for _ in positions]
    for i, pos1 in enumerate(positions):
        for j, pos2 in enumerate(positions):
            if i >= j:
                continue
            y_max = max(pos2[0], pos1[0])
            y_min = min(pos2[0], pos1[0])
            x_max = max(pos2[1], pos1[1])
            x_min = min(pos2[1], pos1[1])
            dist = y_max - y_min + x_max - x_min
            cols_count = sum(map(lambda c: c in range(x_min, x_max + 1), empty_cols))
            rows_count = sum(map(lambda r: r in range(y_min, y_max + 1), empty_rows))
            dist_with_spaces = dist + cols_count * (empty_space_size - 1) + rows_count * (empty_space_size - 1)
            all_distances[i][j] = min(all_distances[i][j], dist_with_spaces)
            all_distances[j][i] = all_distances[i][j]
    result = 0
    for y, row in enumerate(all_distances):
        for x, value in enumerate(row):
            if x < y:
                result += value
    return result


def main():
    assert 374 == solve(puzzle.examples[0].input_data, 2)
    print("part1 example OK")

    puzzle.answer_a = solve(puzzle.input_data, 2)
    print("part1 OK")

    assert 1030 == solve(puzzle.examples[0].input_data, 10)
    print("part2 example 1 OK")

    assert 8410 == solve(puzzle.examples[0].input_data, 100)
    print("part2 example 2 OK")

    puzzle.answer_b = solve(puzzle.input_data, 1000000)
    print("part2 OK")


if __name__ == '__main__':
    main()
