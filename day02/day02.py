import re
from collections import defaultdict
from functools import reduce

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=2)


def parse(data_input):
    games = []
    for line in data_input.split("\n"):
        game_input, cubes_input = line.split(":")
        subsets_intput = cubes_input.split(";")
        subsets = []
        for subset in subsets_intput:
            dices_input = subset.split(",")
            cubes = []
            for dice_input in dices_input:
                dice_match = re.search(" (?P<dices>([0-9]+)) (?P<color>(red|green|blue))", dice_input)
                dice = int(dice_match.group("dices"))
                color = dice_match.group("color")
                cubes.append((dice, color))
            subsets.append(cubes)
        games.append(subsets)
    return games


def part1(data_input):
    games = parse(data_input)
    possible_cubes = {
        'red': 12,
        'green': 13,
        "blue": 14
    }
    possible_games = 0
    for idx, game in enumerate(games):
        possible = True
        for subset in game:
            for cubes, color in subset:
                limit = possible_cubes.get(color)
                if limit < cubes:
                    possible = False
        if possible:
            possible_games += idx + 1
    return possible_games


def part2(data_input):
    games = parse(data_input)
    result = 0
    for game in games:
        min_dices = defaultdict(int)
        for subset in game:
            for cubes, color in subset:
                min_dices[color] = max(min_dices[color], cubes)
        result += reduce(lambda x, y: x * y, min_dices.values())
    return result


def main():
    assert 8 == part1(puzzle.examples[0].input_data)

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 ok")

    assert 2286 == part2(puzzle.examples[0].input_data)

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
