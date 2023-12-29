from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=18)


def parse(input_data):
    result = []
    for line in input_data.split("\n"):
        direction, length, color = line.split(" ")
        length = int(length)
        color = color[1:-1]
        result.append((direction, length, color))
    return result


def shoelace(vectors):
    area = 0
    vectors.append(vectors[0])
    for i in range(len(vectors) - 1):
        x1, y1 = vectors[i]
        x2, y2 = vectors[i + 1]
        area += x1 * y2
        area -= x2 * y1
    return area / 2


def is_clockwise(direction, next_dir):
    clockwise = [
        ("U", "R"),
        ("R", "D"),
        ("D", "L"),
        ("L", "U"),
    ]
    return (direction, next_dir) in clockwise


def segments_to_vectors(segments):
    points = []
    vy, vx = 0, 0

    def get_next_dir(idx):
        return segments[(idx + 1) % len(segments)][0]

    def get_prev_dir(idx):
        return segments[idx - 1][0]

    for i in range(len(segments)):
        d, l, c = segments[i]
        next_dir = get_next_dir(i)
        prev_dir = get_prev_dir(i)
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
    return shoelace(vectors)


def decode(color):
    d = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }.get(color[-1])
    length = int(color[1:-1], 16)
    return d, length, None


def part2(input_data):
    segments = parse(input_data)
    decoded_segments = []
    for seg in segments:
        decoded_segments.append(decode(seg[2]))
    vectors = segments_to_vectors(decoded_segments)
    return shoelace(vectors)


def main():
    assert shoelace([(1, 6), (3, 1), (7, 2), (4, 4), (8, 5)]) == 16.5
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
