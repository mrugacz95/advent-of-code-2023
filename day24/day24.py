from re import findall

from utils import read_input

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=24)


def parse(input_data):
    particles = []
    for line in input_data.split("\n"):
        pos, v = line.split(" @ ")
        pos = list(map(int, pos.split(", ")))
        v = list(map(int, v.split(", ")))
        particles.append((pos, v))
    return particles


def to_function(particle):
    pos, v = particle
    vx, vy, _ = v
    x, y, _ = pos
    return vy / vx, -1, - (vy * x) / vx + y  # result[0] * x + result[1] * y + c


def intersection(f1, f2):
    a1, b1, c1 = f1
    a2, b2, c2 = f2
    if a1 * b2 - a2 * b1 == 0:  # parallel
        return None, None
    return (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1), (c1 * a2 - c2 * a1) / (a1 * b2 - a2 * b1)


def is_in_future(particle, point):
    pos, v = particle
    vx, vy, _ = v
    x, y, _ = pos
    px, py = point
    if vx > 0 and px > x:
        return True
    if vx < 0 and px < x:
        return True
    return False


def part1(input_data, min_pos, max_pos):
    particles = parse(input_data)
    counter = 0
    for i, p1 in enumerate(particles):
        for p2 in particles[i + 1:]:
            if p1 == p2:
                continue
            print(f'testing {p1} {p2}')
            func1 = to_function(p1)
            func2 = to_function(p2)
            x, y = intersection(func1, func2)
            if x is None or y is None:
                print("Dont intersect")
            elif not is_in_future(p1, (x, y)):
                print(f'({x}, {y}) not in future of A')
            elif not is_in_future(p2, (x, y)):
                print(f'({x}, {y}) not in future of B')
            elif not (min_pos <= x <= max_pos and min_pos <= y <= max_pos):
                print(f'Not in test area -  {x}, {y}')
            else:
                print(f'intersect in future in {x}, {y}')
                counter += 1
    print(counter)
    return counter


def part2(input_data):
    data = parse(input_data)


def main():
    assert 2 == part1(puzzle.examples[0].input_data, 7, 27)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data, 200000000000000, 400000000000000)
    print("part1 OK")

    assert 0 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
