import re
from functools import reduce
from math import sqrt, floor, ceil
from re import findall

from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=6)


def parse_part1(input_data):
    lines = input_data.split("\n")
    time = map(int, re.findall("[0-9]+", lines[0]))
    dist = map(int, re.findall("[0-9]+", lines[1]))
    return time, dist


def part1(input_data):
    time, dist = parse_part1(input_data)
    winning_times = []
    for race_time, race_record in zip(time, dist):
        won_ways = 0
        for press_time in range(1, race_time - 1):
            if press_time * (race_time - press_time) > race_record:
                won_ways += 1
        winning_times.append(won_ways)
    return reduce(lambda x, y: x * y, winning_times)


def parse_part2(input_data):
    lines = input_data.split("\n")
    time = int(''.join(re.findall("[0-9]+", lines[0])))
    dist = int(''.join(re.findall("[0-9]+", lines[1])))
    return time, dist


def part2(input_data):
    race_time, race_dist = parse_part2(input_data)
    won_ways = 0
    for press_time in range(1, race_time - 1):
        if press_time * (race_time - press_time) > race_dist:
            won_ways += 1
    return won_ways


def part2_optimised(input_data):
    race_time, race_dist = parse_part2(input_data)
    sqrt_delta = sqrt(pow(race_time, 2.0) - 4.0 * race_dist)
    win_ways = floor((race_time + sqrt_delta) / 2.0) - ceil((race_time - sqrt_delta) / 2.0)
    return win_ways + 1


def main():
    assert 288 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 71503 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")
    assert 71503 == part2_optimised(puzzle.examples[0].input_data)
    print("part2 optimised example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")
    puzzle.answer_b = part2_optimised(puzzle.input_data)
    print("part2 optimised OK")

if __name__ == '__main__':
    main()
