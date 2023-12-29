from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=10)

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

START_SYMBOL = 'S'

PIPES = {
    '|': [UP, DOWN],
    '-': [LEFT, RIGHT],
    'L': [UP, RIGHT],
    'J': [UP, LEFT],
    '7': [LEFT, DOWN],
    'F': [RIGHT, DOWN],
    '.': []
}

SIDES = [UP, DOWN, LEFT, RIGHT]


def parse(input_data):
    data = input_data.split("\n")
    start = None
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == START_SYMBOL:
                start = (y, x)
    assert start is not None, f"No starting node"

    def dfs(start_node):
        visited = []
        nodes = [start_node]
        while True:
            node = nodes.pop()
            symbol = data[node[0]][node[1]]
            if node in visited and symbol != START_SYMBOL:
                continue
            if len(visited) > 1 and node == visited[-2]:  # don't go back after one pipe
                continue
            if len(visited) > 1 and node == start:  # visit something
                return visited
            visited.append(node)
            if symbol == 'S':
                neighbours = [UP, DOWN, LEFT, RIGHT]
            else:
                neighbours = PIPES[symbol]
            for neighbour in neighbours:
                ny, nx = node[0] + neighbour[0], node[1] + neighbour[1]
                if ny < 0 or ny >= len(data) or nx < 0 or nx >= len(data[0]):
                    continue
                nodes.append((ny, nx))
        return None

    loop = dfs(start)
    return loop, data


def part1(input_data):
    loop, board = parse(input_data)
    return len(loop) // 2


def part2(input_data):
    loop, board = parse(input_data)
    # scale up the map x2 and mark pipes in loop
    mask = [[False for _ in range(2 * len(board[0]))] for _ in range(2 * len(board))]
    for idx, (ny, nx) in enumerate(loop + [loop[0]]):
        py, px = loop[idx - 1]
        cy, cx = (ny, nx)
        if py > cy:
            py, cy = cy, py
        if px > cx:
            px, cx = cx, px
        if py != cy:
            for y in range(2 * py, 2 * cy + 1):
                mask[y][px * 2] = True
        elif px != cx:
            for x in range(2 * px, 2 * cx + 1):
                mask[py * 2][x] = True
    if mask[0][0]:
        raise RuntimeError("Left top corner is occupies by pipe")
    # bff from corner and mark
    queue = [(0, 0)]
    while len(queue) > 0:
        y, x = queue.pop()
        if mask[y][x]:
            continue
        mask[y][x] = True

        for side in SIDES:
            ny, nx = y + side[0], x + side[1]
            if ny < 0 or ny >= len(mask) or nx < 0 or nx >= len(mask[0]):
                continue
            if not mask[ny][nx]:
                queue.append((ny, nx))

    # for line in mask:
    #     for c in line:
    #         print('X' if c else '.', end='')
    #     print()
    # print("\n")

    inside = 0
    for y, line in enumerate(board):
        for x, char in enumerate(line):
            if not mask[y * 2][x * 2]:
                inside += 1
    return inside


def main():
    part1_example1 = (".....\n"
                      ".S-7.\n"
                      ".|.|.\n"
                      ".L-J.\n"
                      ".....")
    assert 4 == part1(part1_example1)
    print("part1 example 1 OK")

    part1_example2 = ("7-F7-\n"
                      ".FJ|7\n"
                      "SJLL7\n"
                      "|F--J\n"
                      "LJ.LJ")

    assert 8 == part1(part1_example2)
    print("part1 example 2 OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    part2_example1 = ("...........\n"
                      ".S-------7.\n"
                      ".|F-----7|.\n"
                      ".||.....||.\n"
                      ".||.....||.\n"
                      ".|L-7.F-J|.\n"
                      ".|..|.|..|.\n"
                      ".L--J.L--J.\n"
                      "...........")

    assert 4 == part2(part2_example1)
    print("part2 example 1 OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
