from collections import deque, defaultdict

from aocd.models import Puzzle

from day17.day17 import in_bounds

puzzle = Puzzle(year=2023, day=23)

NEIGHBOURS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def can_pass(dy, dx, char):
    return ((char == '<' and dx != 1) or
            (char == '>' and dx != -1) or
            (char == '^' and dy != 1) or
            (char == 'v' and dy != -1))


def exit_pos(board):
    return len(board) - 1, len(board[0]) - 2


def find_corridor_end(board, sy, sx):
    y, x = sy, sx
    length = 0
    visited = set()
    while True:
        visited.add((y, x))
        length += 1
        for dy, dx in NEIGHBOURS:
            ny, nx = y + dy, x + dx
            if (ny, nx) in visited:
                continue
            if in_bounds(board, ny, nx):
                nc = board[ny][nx]
                if nc == '.' and (ny, nx) == exit_pos(board):
                    return ny, nx, length
                if nc == '#':
                    continue
                if nc == '.':  # move to next node
                    y, x = ny, nx
                    break
                if can_pass(dy, dx, nc):  # corridor ended
                    return y, x, length


SLOPES = ['>', '<', '^', 'v']


def parse(input_data):
    board = [list(row) for row in input_data.split("\n")]
    graph = defaultdict(list)
    queue = deque([(0, 1)])
    visited = set()
    while len(queue) > 0:
        pos_y, pos_x = queue.popleft()
        if (pos_y, pos_x) in visited:
            continue
        visited.add((pos_y, pos_x))
        ey, ex, el = find_corridor_end(board, pos_y, pos_x)
        if (ey, ex) == exit_pos(board):  # add exit node
            graph[(pos_y, pos_x)].append((ey, ex, el))
            continue
        for dy, dx in NEIGHBOURS:
            ny, nx = ey + dy, ex + dx
            nc = board[ny][nx]
            if nc in SLOPES and can_pass(dy, dx, nc):
                next_corridor_y, next_corridor_x = ny + dy, nx + dx
                graph[(pos_y, pos_x)].append((next_corridor_y, next_corridor_x, el + 1))  # +1 to add slope length
                queue.append((next_corridor_y, next_corridor_x))
    return graph, board


def print_board(board):
    print('\n'.join([''.join(row) for row in board]))


def find_longest_path(graph, start_node, exit_node):
    def dfs(node, dist, visited):
        if node in visited:
            return -float('inf')
        if node == exit_node:
            return dist
        visited.add(node)
        max_dist = -float('inf')
        for (ny, nx, nl) in graph[node]:
            max_dist = max(max_dist, dfs((ny, nx), dist + nl, visited))
        visited.remove(node)
        return max_dist

    return dfs(start_node, 0, set())


def part1(input_data):
    graph, board = parse(input_data)
    # print_board(board)
    return find_longest_path(graph, (0, 1), exit_pos(board))


def part2(input_data):
    graph, board = parse(input_data)
    bidirectional_graph = defaultdict(list)
    for (ny, nx), edges in graph.items():
        for ey, ex, el in edges:
            bidirectional_graph[(ny, nx)].append((ey, ex, el))
            bidirectional_graph[(ey, ex)].append((ny, nx, el))
    return find_longest_path(bidirectional_graph, (0, 1), exit_pos(board))


def main():
    assert 94 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 154 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
