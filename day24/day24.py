from aocd.models import Puzzle
from z3 import Int, Solver

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


def check_intersection(p1, p2, debug=False):
    func1 = to_function(p1)
    func2 = to_function(p2)
    x, y = intersection(func1, func2)
    if x is None or y is None:
        if debug: print("Dont intersect")
        return None, None
    elif not is_in_future(p1, (x, y)):
        if debug: print(f'({x}, {y}) not in future of A')
        return None, None
    elif not is_in_future(p2, (x, y)):
        if debug: print(f'({x}, {y}) not in future of B')
        return None, None
    return x, y


def part1(input_data, min_pos, max_pos, debug=False):
    particles = parse(input_data)
    counter = 0
    for i, p1 in enumerate(particles):
        for p2 in particles[i + 1:]:
            if p1 == p2:
                continue
            if debug: print(f'testing {p1} {p2}')
            x, y = check_intersection(p1, p2)
            if x is None or y is None:
                continue
            if not (min_pos <= x <= max_pos and min_pos <= y <= max_pos):
                if debug: print(f'Not in test area -  {x}, {y}')
            else:
                if debug: print(f'intersect in future in {x}, {y}')
                counter += 1
    if debug: print(counter)
    return counter

def part2(input_data):
    particles = parse(input_data)
    v0_x = Int('v0_x')
    v0_y = Int('v0_y')
    v0_z = Int('v0_z')
    p0_x = Int('p0_x')
    p0_y = Int('p0_y')
    p0_z = Int('p0_z')
    s = Solver()
    for i, ((pos_x, pos_y, pos_z), (vx, vy, vz)) in enumerate(particles):
        t = Int(f't{i}')  # collision time
        s.add(p0_x + v0_x * t == vx * t + pos_x)
        s.add(p0_y + v0_y * t == vy * t + pos_y)
        s.add(p0_z + v0_z * t == vz * t + pos_z)
    s.check()
    m = s.model()
    print(m)
    return m[p0_x].as_long() + m[p0_y].as_long() + m[p0_z].as_long()


def main():
    assert 2 == part1(puzzle.examples[0].input_data, 7, 27)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data, 200000000000000, 400000000000000)
    print("part1 OK")

    assert 47 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
