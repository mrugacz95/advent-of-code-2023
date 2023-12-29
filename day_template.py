from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=-1)


def parse(input_data):
    return input_data.split("\n")


def part1(input_data):
    data = parse(input_data)
    return -1


def part2(input_data):
    data = parse(input_data)
    return -1


def main():
    assert 0 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 0 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
