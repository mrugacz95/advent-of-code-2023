import re
from re import findall
from typing import Set, Tuple, List

from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=4)


def parse(input) -> List[Tuple[Set[int], Set[int]]]:
    lines = input.split("\n")
    parsed_cards = []
    for line in lines:
        _, cards = re.split(": +", line)
        winning, appeared = re.split(" \| +", cards)
        winning_number = set(map(lambda x: int(x), re.split(" +", winning)))
        appeared_number = set(map(lambda x: int(x), re.split(" +", appeared)))
        parsed_cards.append((winning_number, appeared_number))
    return parsed_cards


def part1(input):
    cards = parse(input)
    points = 0
    for winning, appeared in cards:
        winning_numbers = len(winning.intersection(appeared))
        if winning_numbers > 0:
            points += pow(2, winning_numbers - 1)
    return points


def part2(input):
    cards = parse(input)
    owned_cards = [1 for _ in cards]
    points = 0
    for idx, cards_amount in enumerate(owned_cards):
        winning, appeared = cards[idx]
        winning_numbers = len(winning.intersection(appeared))
        for i in range(idx + 1, idx + 1 + winning_numbers):
            owned_cards[i] += cards_amount
    return sum(owned_cards)


def main():
    assert 13 == part1(puzzle.examples[0].input_data)

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 30 == part2(puzzle.examples[0].input_data)

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
