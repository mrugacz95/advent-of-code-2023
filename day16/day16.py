from enum import Enum
from typing import Set, Tuple

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=16)


def parse(input_data):
    return input_data.split("\n")


class Dir(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def print_beams(board, visited: Set[Tuple[int, int, Dir]]):
    result = []
    for row in board:
        result.append(list(row))
    for py, px, d in visited:
        char = {
            Dir.UP: "^",
            Dir.DOWN: "v",
            Dir.LEFT: "<",
            Dir.RIGHT: ">",
        }.get(d)
        if result[py][px] == '.':
            result[py][px] = char
    print('\n'.join([''.join(row) for row in result]), end="\n\n")


def simulate_beam(board, start_beam: Tuple[int, int, Dir]):
    queue = {start_beam}
    visited = set()
    while len(queue) != 0:
        pos_y, pos_x, direction = queue.pop()
        if (pos_y, pos_x, direction) in visited:
            continue
        visited.add((pos_y, pos_x, direction))
        new_pos_y, new_pos_x = {
            Dir.UP: (pos_y - 1, pos_x),
            Dir.DOWN: (pos_y + 1, pos_x),
            Dir.RIGHT: (pos_y, pos_x + 1),
            Dir.LEFT: (pos_y, pos_x - 1)
        }.get(direction)
        if not (0 <= new_pos_y < len(board) and 0 <= new_pos_x < len(board[0])):
            continue
        mirror = board[new_pos_y][new_pos_x]
        if mirror == ".":
            queue.add((new_pos_y, new_pos_x, direction))
        elif mirror == "/":
            new_direction = {
                Dir.UP: Dir.RIGHT,
                Dir.DOWN: Dir.LEFT,
                Dir.LEFT: Dir.DOWN,
                Dir.RIGHT: Dir.UP
            }.get(direction)
            queue.add((new_pos_y, new_pos_x, new_direction))
        elif mirror == "\\":
            new_direction = {
                Dir.UP: Dir.LEFT,
                Dir.DOWN: Dir.RIGHT,
                Dir.LEFT: Dir.UP,
                Dir.RIGHT: Dir.DOWN
            }.get(direction)
            queue.add((new_pos_y, new_pos_x, new_direction))
        elif mirror == "|":
            if direction == Dir.UP or direction == Dir.DOWN:
                queue.add((new_pos_y, new_pos_x, direction))
            else:
                queue.add((new_pos_y, new_pos_x, Dir.UP))
                queue.add((new_pos_y, new_pos_x, Dir.DOWN))
        elif mirror == "-":
            if direction == Dir.LEFT or direction == Dir.RIGHT:
                queue.add((new_pos_y, new_pos_x, direction))
            else:
                queue.add((new_pos_y, new_pos_x, Dir.LEFT))
                queue.add((new_pos_y, new_pos_x, Dir.RIGHT))
        # print_beams(data, visited)
    lighted = set(map(lambda beam: (beam[0], beam[1]), visited))
    return len(lighted) - 1  # remove starting beam


def part1(input_data):
    data = parse(input_data)
    lighted = simulate_beam(data, (0, -1, Dir.RIGHT))
    return lighted


def part2(input_data):
    data = parse(input_data)
    max_light = 0
    for y in range(len(data)):
        left = simulate_beam(data, (y, -1, Dir.RIGHT))
        right = simulate_beam(data, (y, -1, Dir.LEFT))
        max_light = max(max_light, left, right)
    for x in range(len(data[0])):
        top = simulate_beam(data, (-1, x, Dir.DOWN))
        bot = simulate_beam(data, (len(data), x, Dir.UP))
        max_light = max(max_light, top, bot)
    return max_light


def main():
    assert 46 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 51 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
