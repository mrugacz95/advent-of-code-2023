from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=18)


def parse(input_data):
    result = []
    for line in input_data.split("\n"):
        dir, length, color = line.split(" ")
        length = int(length)
        color = color[1:-1]
        result.append((dir, length, color))
    return result


def shoelance(vectors):
    area = 0
    vectors.append(vectors[0])
    for x1, y2 in zip(map(lambda v: v[0], vectors[:-1]), map(lambda v: v[1], vectors[1:])):
        area += x1 * y2
    for y2, x1 in zip(map(lambda v: v[0], vectors[1:]), map(lambda v: v[1], vectors[:-1])):
        area -= x1 * y2
    return area / 2


def is_clockwise(dir, next_dir):
    clockwise = [
        ("U", "R"),
        ("R", "D"),
        ("D", "L"),
        ("L", "U"),
    ]
    return (dir, next_dir) in clockwise


def segments_to_vectors(segments):
    points = []
    vy, vx = 0, 0

    def get_next_dir(i):
        return segments[(i + 1) % len(segments)][0]

    def get_prev(i):
        return segments[i - 1][0]

    for i in range(len(segments)):
        d, l, c = segments[i]
        next_dir = get_next_dir(i)
        prev_dir = get_prev(i)
        is_prev_cloc = 0 if is_clockwise(prev_dir, d) else -1
        is_next_cloc = 1 if is_clockwise(d, next_dir) else 0
        dy, dx = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1),
        }.get(d)
        l += is_next_cloc + is_prev_cloc
        vy, vx = vy + l * dy, vx + l * dx
        points.append((vy, vx))
    return points


def part1(input_data):
    segments = parse(input_data)
    vectors = segments_to_vectors(segments)
    return shoelance(vectors)


def decode(hex):
    d = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }.get(hex[-1])
    length = int(hex[1:-1], 16)
    return d, length, None


def part2(input_data):
    segments = parse(input_data)
    decoded_segments = []
    for seg in segments:
        decoded_segments.append(decode(seg[2]))
    vectors = segments_to_vectors(decoded_segments)
    return shoelance(vectors)


def main():
    assert shoelance([(1, 6), (3, 1), (7, 2), (4, 4), (8, 5)]) == 16.5
    assert segments_to_vectors([('U', 3, '-'), ('R', 5, '-'),
                                ('D', 3, '-'), ('L', 5, '-')]) == [(4, 0), (4, 6), (0, 6), (0, 0)]
    assert 20 == part1("U 3 -\n"
                       "R 4 -\n"
                       "D 3 -\n"
                       "L 4 -")

    # ###
    # ###
    # ##
    # ###
    # ###

    assert 14 == part1("U 4 -\n"
                       "R 2 -\n"
                       "D 1 -\n"
                       "L 1 -\n"
                       "D 2 -\n"
                       "R 1 -\n"
                       "D 1 -\n"
                       "L 2 -")
    print("part1 tests OK")

    assert 62 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert decode('#70c710') == ('R', 461937, None)

    print("part2 tests OK")

    assert 952408144115 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
