import re
from re import findall

from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=3)

eight_neighbours = [
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
]


def adjacent(y, x, size_x, size_y, neighbourhood):
    result = []
    for dy, dx in neighbourhood:
        ny, nx = dy + y, dx + x
        if ny >= size_y or ny < 0:
            continue
        if nx >= size_x or nx < 0:
            continue
        result.append((ny, nx))
    return result


def get_number(string, position):
    start_char = string[position]
    prefix = ""
    for x in range(position - 1, -1, -1):
        if string[x].isdigit():
            prefix = string[x] + prefix
        else:
            break
    suffix = ""
    for x in range(position + 1, len(string)):
        if string[x].isdigit():
            suffix += string[x]
        else:
            break
    number = prefix + start_char + suffix
    return number, len(suffix)  # return number and how long it is after encountered digit


def part1(input):
    board = input.split('\n')
    mask = [[False for x in line] for line in board]
    # find adjacent numbers
    for y, line in enumerate(board):
        for x, c in enumerate(line):
            if not c.isdigit() and c != '.':
                neighbours = adjacent(y, x, len(board), len(line), eight_neighbours)
                for ny, nx in neighbours:
                    if board[ny][nx].isdigit():
                        mask[ny][nx] = True  # mark mask if any adjacent number
    sum = 0
    for y, line in enumerate(mask):
        x = 0
        while x < len(line):
            if line[x] is True and board[y][x].isdigit():
                number, length_after = get_number(board[y], x)
                sum += int(number)
                x += length_after  # skip number to count it once
            x += 1
    return sum


def part2(input):
    board = input.split('\n')
    mask = [[-1 for x in line] for line in board]  # mask allowing mapping y,x to number
    numbers = []  # list of all available numbers
    for y, line in enumerate(board):
        for group in re.finditer(r'[0-9]+', line):
            number_start = group.span()[0]
            number_end = group.span()[1]
            number_len = number_end - number_start
            mask[y][number_start:number_end] = [len(numbers) for _ in range(number_len)]
            numbers.append(int(group.group()))
    sum = 0
    for y, line in enumerate(board):
        for x, c in enumerate(line):
            if c == '*':
                number_indices = set()  # avoid duplication with set
                neighbours = adjacent(y, x, len(board), len(line), eight_neighbours)
                for ny, nx in neighbours:
                    if board[ny][nx].isdigit():
                        number_indices.add(mask[ny][nx])
                if len(number_indices) == 2:
                    neighbour_numbers = [numbers[idx] for idx in number_indices]
                    sum += neighbour_numbers[0] * neighbour_numbers[1]
    return sum


def main():
    assert 4361 == part1(puzzle.examples[0].input_data)

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 ok")

    assert 467835 == part2(puzzle.examples[0].input_data)

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
