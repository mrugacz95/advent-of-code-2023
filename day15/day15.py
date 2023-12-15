import re
from collections import deque, OrderedDict
from functools import cache
from re import findall

from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=15)


def parse(input_data):
    return input_data.split(",")


@cache
def holiday_hash(string):
    value = 0
    for char in string:
        value = ((value + ord(char)) * 17) % 256
    return value


def part1(input_data):
    data = parse(input_data)
    result = 0
    for step in data:
        result += holiday_hash(step)
    return result


def decode_step(step):
    groups = re.search(r'(?P<label>([a-z]+))(?P<op>([-=]))(?P<number>([0-9]+)?)', step)
    number = groups.group('number')
    return groups.group('label'), groups.group('op'), int(number) if number != '' else None


def print_boxes(boxes):
    for box_idx, box in enumerate(boxes):
        if len(box) == 0:
            continue
        print('Box', box_idx, end=' ')
        for lens in box.items():
            print(lens, end=", ")
        print()
    print()


def calc_power(boxes):
    power = 0
    for box_idx, box in enumerate(boxes):
        for lens_id, lens in enumerate(box.items()):
            power += (box_idx + 1) * (lens_id + 1) * lens[1]
    return power


def part2(input_data):
    data = parse(input_data)
    boxes = [OrderedDict() for _ in range(256)]
    for step in data:
        label, op, focal_length = decode_step(step)
        box_number = holiday_hash(label)
        if op == '-':
            if label in boxes[box_number]:
                del boxes[box_number][label]
        elif op == '=':
            boxes[box_number][label] = focal_length
        else:
            raise RuntimeError(f"Unknown operation {op}")
        print_boxes(boxes)

    return calc_power(boxes)


def main():
    assert 52 == holiday_hash("HASH")
    assert 1320 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert ('rm', '=', 6) == decode_step("rm=6")
    assert ('op', '-', None) == decode_step("op-")
    assert 145 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
