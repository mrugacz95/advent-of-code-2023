import re
from functools import reduce
from re import findall

from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=8)


def parse(input_data):
    moves, input_lines = input_data.split("\n\n")
    graph = {}
    for line in input_lines.split("\n"):
        node, left, right = line[:3], line[7:10], line[12:15]
        graph[node] = (left, right)
    return moves, graph


def part1(input_data):
    moves, graph = parse(input_data)
    step = 0
    node = 'AAA'
    while node != 'ZZZ':
        move = moves[step % len(moves)]
        if move == 'L':
            node = graph[node][0]
        elif move == 'R':
            node = graph[node][1]
        else:
            raise RuntimeError('Unknown move')
        step += 1
    return step


def part2(input_data):
    moves, graph = parse(input_data)
    nodes = list(filter(lambda x: x[-1] == 'A', graph.keys()))
    step = 0
    while not all(map(lambda x: x[-1] == 'Z', nodes)):
        move = moves[step % len(moves)]
        new_nodes = []
        for node in nodes:
            if move == 'L':
                new_nodes.append(graph[node][0])
            elif move == 'R':
                new_nodes.append(graph[node][1])
            else:
                raise RuntimeError('Unknown move')
        step += 1
        nodes = new_nodes
    return step


def walk_from_node(node, moves, graph):
    step = 0
    while node[-1] != 'Z':
        move = moves[step % len(moves)]
        node = graph[node][0 if move == 'L' else 1]
        step += 1
    return step


def gcd(a, b):
    """
    Source: https://en.wikipedia.org/wiki/Euclidean_algorithm#Implementations
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def lcm(a, b):
    """
    Source: https://en.wikipedia.org/wiki/Least_common_multiple#Calculation
    """
    return a * b / gcd(a, b)


def part2_faster(input_data):
    moves, graph = parse(input_data)
    nodes = list(filter(lambda x: x[-1] == 'A', graph.keys()))
    nodes_length = []
    for node in nodes:
        length = walk_from_node(node, moves, graph)
        nodes_length.append(length)
    steps = int(reduce(lambda x, y: lcm(x, y), nodes_length))
    return steps


def main():
    assert 2 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    example2 = ("LR\n\n"
                "11A = (11B, XXX)\n"
                "11B = (XXX, 11Z)\n"
                "11Z = (11B, XXX)\n"
                "22A = (22B, XXX)\n"
                "22B = (22C, 22C)\n"
                "22C = (22Z, 22Z)\n"
                "22Z = (22B, 22B)\n"
                "XXX = (XXX, XXX)")
    assert 6 == part2(example2)
    print("part2 example OK")

    assert gcd(21, 3) == 3
    assert lcm(21, 6) == 42
    assert 6 == part2_faster(example2)
    print("part2 faster example OK")

    puzzle.answer_b = part2_faster(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
