from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=13)


def parse(input_data):
    data = input_data.split("\n\n")
    return [example.split("\n") for example in data]


# Some visual help

# 0 #
# 1 #
# 2 .
# 3 #
#     --- 3 ---
# 4 #
# 5 .
# 6 #

def find_horizontal_reflection(example, skip=None):
    for reflection_line in range(len(example) - 1):
        match = True
        if reflection_line + 1 == skip:
            continue
        for col_id in range(0, min(reflection_line + 1, len(example) - reflection_line - 1)):
            if example[reflection_line - col_id] != example[reflection_line + col_id + 1]:
                match = False
                break
        if match:
            return reflection_line + 1
    return None


def flip(example):
    def get_column(col_id):
        return list(map(lambda x: x[col_id], example))

    rows = []
    for i in range(len(example[0])):
        rows.append(get_column(i))
    return rows


def calculate_reflection(example):
    horizontal = find_horizontal_reflection(example)
    if horizontal is None:
        vertical = find_horizontal_reflection(flip(example))
    else:
        vertical = None
    return horizontal, vertical


def calc_value(horizontal, vertical):
    return (100 * horizontal if horizontal is not None else 0) + (vertical if vertical is not None else 0)


def part1(input_data):
    data = parse(input_data)

    all_reflections = 0
    for example in data:
        horizontal, vertical = calculate_reflection(example)
        all_reflections += calc_value(horizontal, vertical)
    return all_reflections


def replace(example, y, x, symbol):
    changes = []
    for i, row in enumerate(example):
        if i == y:
            changes.append(example[i][:x] + symbol + example[i][x + 1:])
        else:
            changes.append(example[i])
    return changes


def calculate_reflection_with_forbidden(example, forbidden_horizontal, forbidden_vertical):
    horizontal = find_horizontal_reflection(example, forbidden_horizontal)
    if horizontal is None:
        vertical = find_horizontal_reflection(flip(example), forbidden_vertical)
    else:
        vertical = None
    return horizontal, vertical


def part2(input_data):
    data = parse(input_data)
    all_reflections = 0
    for example in data:
        (init_ref_hor, init_ref_vert) = calculate_reflection(example)
        found = False
        for y, row in enumerate(example):
            for x, symbol in enumerate(row):
                other_symbol = {
                    '.': '#',
                    '#': '.'
                }.get(symbol)
                replaced_example = replace(example, y, x, other_symbol)
                changed_reflection = calculate_reflection_with_forbidden(replaced_example, init_ref_hor, init_ref_vert)
                if (init_ref_hor, init_ref_vert) != changed_reflection and changed_reflection != (None, None):
                    all_reflections += calc_value(*changed_reflection)
                    found = True
                    break
            if found:
                break
        if not found:
            raise RuntimeError("No new reflection found")
    return all_reflections


def main():
    assert 405 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    to_replace = ['.#', '#.']
    assert replace(['.#', '#.'], 1, 1, '#') == ['.#', '##']
    assert to_replace == ['.#', '#.']

    assert 400 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    assert part2("#####..\n"
                 "..#.##.\n"
                 "..#.##.\n"
                 "#####..\n"
                 "##.....\n"
                 "###.##.\n"
                 "#..#.##\n"
                 "######.\n"
                 "..##.##\n"
                 "..#.#..\n"
                 "..#####") == 1

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
