from enum import Enum
from heapq import heappush, heappop

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=17)


def parse(input_data):
    return [list(map(int, line)) for line in input_data.split("\n")]


class Dir(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def __lt__(self, other):
        return self.value < other.value


def turn_left(direction):
    return {
        Dir.UP: Dir.LEFT,
        Dir.RIGHT: Dir.UP,
        Dir.DOWN: Dir.RIGHT,
        Dir.LEFT: Dir.DOWN
    }.get(direction)


def turn_right(direction):
    return {
        Dir.UP: Dir.RIGHT,
        Dir.RIGHT: Dir.DOWN,
        Dir.DOWN: Dir.LEFT,
        Dir.LEFT: Dir.UP
    }.get(direction)


def get_delta(direction):
    return {
        Dir.UP: (-1, 0),
        Dir.RIGHT: (0, 1),
        Dir.DOWN: (1, 0),
        Dir.LEFT: (0, -1)
    }.get(direction)


def in_bounds(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board[0])


def print_board_with_path(board, prev):
    with_path = [[x for x in line] for line in board]
    y = len(board) - 1
    x = len(board[0]) - 1
    while not (y == 0 and x == 0):
        prev_y, prev_x, direction = prev[y][x]
        dir_symb = {
            Dir.UP: '^',
            Dir.DOWN: 'v',
            Dir.RIGHT: '>',
            Dir.LEFT: '<',
        }.get(direction)
        with_path[y][x] = dir_symb
        y, x, = prev_y, prev_x
    print('path')
    print('\n'.join([','.join([str(x).rjust(4) for x in line]) for line in with_path]))


def find_path(board):
    queue = []
    # cost, y, x, straight, dir, prev_y, prev_x, prev_dir
    heappush(queue, (0, 0, 0, 4, Dir.RIGHT, -1, -1))  # 4 because first 4 moves can be in right
    visited = set()
    lowest_cost = float('inf')
    while len(queue) != 0:
        cost, y, x, straight, direction, prev_y, prev_x = heappop(queue)
        if (y, x, straight, direction) in visited:
            continue
        visited.add((y, x, straight, direction))
        # left
        new_dir = turn_left(direction)
        dy, dx = get_delta(new_dir)
        new_y, new_x = y + dy, x + dx
        if in_bounds(board, new_y, new_x):
            new_cost = cost + board[new_y][new_x]
            heappush(queue, (new_cost, new_y, new_x, 3, new_dir, y, x))
        # right
        new_dir = turn_right(direction)
        dy, dx = get_delta(new_dir)
        new_y, new_x = y + dy, x + dx
        if in_bounds(board, new_y, new_x):
            new_cost = cost + board[new_y][new_x]
            heappush(queue, (new_cost, new_y, new_x, 3, new_dir, y, x))
        # straight
        if straight > 1:
            dy, dx = get_delta(direction)
            new_y, new_x = y + dy, x + dx
            if in_bounds(board, new_y, new_x):
                new_cost = cost + board[new_y][new_x]
                heappush(queue, (new_cost, new_y, new_x, straight - 1, direction, y, x))
        if y == len(board) - 1 and x == len(board[0]) - 1:
            lowest_cost = cost
            break
    return lowest_cost


def part1(input_data):
    # print(input_data)
    board = parse(input_data)
    return find_path(board)


def find_ultra_path(board):
    queue = []
    # cost, y, x, straight, dir, prev_y, prev_x, prev_dir
    heappush(queue, (0, 0, 0, -1, Dir.RIGHT, -1, -1))
    visited = set()
    lowest_cost = float('inf')
    min_moves = 3  # one less
    max_moves = 9  # one less
    while len(queue) != 0:
        cost, y, x, straight, direction, prev_y, prev_x = heappop(queue)
        if (y, x, straight, direction) in visited:
            continue
        visited.add((y, x, straight, direction))
        # left
        if straight >= min_moves:
            new_dir = turn_left(direction)
            dy, dx = get_delta(new_dir)
            new_y, new_x = y + dy, x + dx
            if in_bounds(board, new_y, new_x):
                new_cost = cost + board[new_y][new_x]
                heappush(queue, (new_cost, new_y, new_x, 0, new_dir, y, x))
        # right
        if straight >= min_moves:
            new_dir = turn_right(direction)
            dy, dx = get_delta(new_dir)
            new_y, new_x = y + dy, x + dx
            if in_bounds(board, new_y, new_x):
                new_cost = cost + board[new_y][new_x]
                heappush(queue, (new_cost, new_y, new_x, 0, new_dir, y, x))
        # straight
        if straight < max_moves:
            dy, dx = get_delta(direction)
            new_y, new_x = y + dy, x + dx
            if in_bounds(board, new_y, new_x):
                new_cost = cost + board[new_y][new_x]
                heappush(queue, (new_cost, new_y, new_x, straight + 1, direction, y, x))
        if y == len(board) - 1 and x == len(board[0]) - 1 and straight >= min_moves:
            lowest_cost = cost
            break
    return lowest_cost


def part2(input_data):
    # print(input_data)
    board = parse(input_data)
    return find_ultra_path(board)


def main():
    example = ("9111999\n"
               "9991111")
    assert 7 == part1(example)
    example = ("9911199\n"
               "1119111")
    assert 9 == part1(example)
    example = ("9111199\n"
               "9999111")
    assert 15 == part1(example)

    example = ("9999999\n"
               "1111111")
    assert 25 == part1(example)

    example = ("91111\n"
               "55555\n"
               "11111\n"
               "99999")
    assert 19 == part1(example)

    example = ("241343\n"
               "321545")
    assert 20 == part1(example)

    example = ("9111991111\n"
               "9991111991")
    assert 12 == part1(example)

    example = ("241343231\n"
               "321545353")
    assert 32 == part1(example)

    print("part1 tests OK")

    assert 102 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    example = ("111111111111\n"
               "999999999991\n"
               "999999999991\n"
               "999999999991\n"
               "999999999991")
    assert 71 == part2(example)
    print("part2 tests OK")

    assert 94 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
