import re
from typing import Set, Tuple, List

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=4)


def parse(data_input) -> List[Tuple[Set[int], Set[int]]]:
    lines = data_input.split("\n")
    parsed_cards = []
    for line in lines:
        _, cards = re.split(": +", line)
        winning, appeared = re.split(r" \| +", cards)
        winning_number = set(map(lambda x: int(x), re.split(" +", winning)))
        appeared_number = set(map(lambda x: int(x), re.split(" +", appeared)))
        parsed_cards.append((winning_number, appeared_number))
    return parsed_cards


def part1(data_input):
    cards = parse(data_input)
    points = 0
    for winning, appeared in cards:
        winning_numbers = len(winning.intersection(appeared))
        if winning_numbers > 0:
            points += pow(2, winning_numbers - 1)
    return points


def part2(data_input):
    cards = parse(data_input)
    owned_cards = [1 for _ in cards]
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
