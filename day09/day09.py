from re import findall

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=9)


def parse(input_data):
    data = []
    for line in input_data.split("\n"):
        number = list(map(int, findall(r"-?\d+", line)))
        data.append(number)
    return data


def find_differences(numbers):
    differences = []
    for i in range(0, len(numbers) - 1):
        differences.append(numbers[i + 1] - numbers[i])
    return differences


def find_all_differences(series):
    sequences = [series]
    while not all(map(lambda x: x == 0, sequences[-1])):
        sequences.append(find_differences(sequences[-1]))
    return sequences


def part1(input_data):
    data = parse(input_data)
    result = 0
    for series in data:
        sequences = find_all_differences(series)
        for i in reversed(range(1, len(sequences))):
            new_number = sequences[i - 1][-1] + sequences[i][-1]
            sequences[i - 1].append(new_number)
        result += sequences[0][-1]
    return result


def part2(input_data):
    data = parse(input_data)
    result = 0
    for series in data:
        sequences = find_all_differences(series)
        for i in reversed(range(1, len(sequences))):
            new_number = sequences[i - 1][0] - sequences[i][0]
            sequences[i - 1].insert(0, new_number)
        result += sequences[0][0]
    return result


def main():
    assert 114 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")
    assert -26 == part1("-5 -6 -7 -8 -9 -10 -11 -12 -13 -14 -15 -16 -17 -18 -19 -20 -21 -22 -23 -24 -25")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 2 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
