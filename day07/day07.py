from collections import Counter
from functools import cmp_to_key

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=7)

FIVE = 7
FOUR = 6
FULL = 5
THREE = 4
TWO_PAIRS = 3
PAIR = 2
HIGH_CARD = 1

FIGURES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARD_VALUE = {f: v for v, f in enumerate(FIGURES)}
EMPTY_COUNTER = Counter({f: 0 for f in FIGURES})


def get_type(cards):
    values = Counter(cards).values()
    if 5 in values:
        return FIVE
    if 4 in values:
        return FOUR
    if 2 in values and 3 in values:
        return FULL
    if 3 in values:
        return THREE
    if Counter(values)[2] == 2:
        return TWO_PAIRS
    if 2 in values:
        return PAIR
    return HIGH_CARD


def compare_cards(lhs, rhs):
    # compare type
    lhs_type = get_type(lhs)
    rhs_type = get_type(rhs)
    if lhs_type != rhs_type:
        return lhs_type - rhs_type
    # compare tie
    for l_card, r_card in zip(lhs, rhs):
        if l_card != r_card:
            l_value = CARD_VALUE[l_card]
            r_value = CARD_VALUE[r_card]
            return l_value - r_value
    return 0


def parse(input_data):
    parsed = []
    for line in input_data.split("\n"):
        cards, bid = line.split(" ")
        parsed.append((cards, int(bid)))
    return parsed


def part1(input_data):
    data = parse(input_data)
    ranked = sorted(data, key=cmp_to_key(lambda lhs, rhs: compare_cards(lhs[0], rhs[0])))
    winnings = 0
    for rank, (cards, bid) in enumerate(ranked):
        winnings += (rank + 1) * bid
    return winnings


CARD_VALUE2 = CARD_VALUE.copy()
CARD_VALUE2['J'] = -1


def get_type_with_jokers(cards):
    if 'J' not in cards:
        return get_type(cards)
    best_type = HIGH_CARD
    for figure in FIGURES:  # not efficient but works like a charm
        replaced = cards.replace('J', figure)
        best_type = max(best_type, get_type(replaced))
    return best_type


def compare_cards_with_jokers(lhs, rhs):
    # compare type
    lhs_type = get_type_with_jokers(lhs)
    rhs_type = get_type_with_jokers(rhs)
    if lhs_type != rhs_type:
        return lhs_type - rhs_type

    for l_card, r_card in zip(lhs, rhs):
        if l_card != r_card:
            l_value = CARD_VALUE2[l_card]
            r_value = CARD_VALUE2[r_card]
            return l_value - r_value
    return 0


def part2(input_data):
    data = parse(input_data)
    ranked = sorted(data, key=cmp_to_key(lambda lhs, rhs: compare_cards_with_jokers(lhs[0], rhs[0])))
    winnings = 0
    for rank, (cards, bid) in enumerate(ranked):
        winnings += (rank + 1) * bid
    return winnings


def main():
    assert get_type('AAAAA') == FIVE
    assert get_type('AA8AA') == FOUR
    assert get_type('23332') == FULL
    assert get_type('TTT98') == THREE
    assert get_type('23432') == TWO_PAIRS
    assert get_type('A23A4') == PAIR
    assert get_type('23456') == HIGH_CARD

    assert compare_cards('23456', 'KTJJT') < 0
    assert compare_cards('32T3K', 'KTJJT') < 0
    assert compare_cards('KTJJT', 'KK677') < 0
    assert compare_cards('KK677', 'T55J5') < 0
    assert compare_cards('T55J5', 'QQQJA') < 0

    assert 6440 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert get_type_with_jokers('QJJQ2') == FOUR

    assert 5905 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
