from re import findall

from utils import read_input

from aocd.models import Puzzle
puzzle = Puzzle(year=2023, day=1)

def part1(input):
    sum = 0
    for line in input.split('\n'):
        digits = list(filter(lambda x: x.isnumeric(), str(line)))
        number = int(digits[0] + digits[-1])
        sum += number
    return sum


def part2(input):
    def text_to_number(number):
        return {
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9'
        }.get(number, number)

    sum = 0
    for line in input.split('\n'):
        digits = findall(r'(?=([1-9]{1}|one|two|three|four|five|six|seven|eight|nine))', str(line))
        first = text_to_number(digits[0])
        last = text_to_number(digits[-1])
        number = int(first + last)
        sum += number
    return sum


def main():
    assert 142 == part1(puzzle.examples[0].input_data)

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 ok")

    input_part2 = ("two1nine\n"
                   "eightwothree\n"
                   "abcone2threexyz\n"
                   "xtwone3four\n"
                   "4nineeightseven2\n"
                   "zoneight234\n"
                   "7pqrstsixteen")

    assert 281 == part2(input_part2)

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")

if __name__ == '__main__':
    main()
