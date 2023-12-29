import re
from collections import deque

from aocd.models import Puzzle
from tqdm import tqdm

puzzle = Puzzle(year=2023, day=22)


class Cube:
    def __init__(self, cube_id: int, start: tuple, end: tuple):
        self.sx, self.sy, self.sz = start
        self.ex, self.ey, self.ez = end
        assert self.sx <= self.ex
        assert self.sy <= self.ey
        assert self.sz <= self.ez
        self.id = cube_id

    def get_ranges(self):
        return [(self.sz, self.ez), (self.sy, self.ey), (self.sx, self.ex)]  # start from z

    def fall(self, cubes):
        cube = self
        while cube.can_fall(cubes):
            cube = cube.fall_by_one()
        # print(f"{self.get_printable_id()} felt by {fall_dist}")
        return cube

    def can_fall(self, cubes):
        if self.sz <= 1:
            return False
        next_pos = self.fall_by_one()
        for other_cube in cubes:
            if other_cube.id == next_pos.id:
                continue
            if next_pos.collide(other_cube):
                return False
        return True

    def collide(self, other: 'Cube') -> bool:
        for cube_range, other_range in zip(self.get_ranges(), other.get_ranges()):
            if not Cube._overlap(cube_range, other_range):
                return False
        return True

    def fall_by_one(self):
        return Cube(self.id, (self.sx, self.sy, self.sz - 1), (self.ex, self.ey, self.ez - 1))

    def get_printable_id(self):
        return chr(self.id + ord('A'))

    def get_supporting_cubes(self, cubes):
        one_below = self.fall_by_one()
        supporting = []
        for cube in cubes:
            if cube.id != self.id:
                if cube.ez + 1 == self.sz:
                    if one_below.collide(cube):
                        supporting.append(cube)
        return supporting

    def __repr__(self):
        return f'Cube({self.id}, {self.sx}, {self.sy}, {self.sz} ~ {self.ex}, {self.ey}, {self.ez})'

    def __copy__(self):
        return Cube(self.id, (self.sx, self.sy, self.sz), (self.ex, self.ey, self.ez))

    def start(self):
        return self.sx, self.sy, self.sz

    def end(self):
        return self.ex, self.ey, self.ez

    def __eq__(self, other):
        return self.id == other.id and self.start() == other.start() and self.end() == other.end()

    def __lt__(self, other):
        return self.sz < other.sz

    @staticmethod
    def _overlap(lhs, rhs):
        lhs_start, lhs_end = lhs
        rhs_start, rhs_end = rhs
        return lhs_end >= rhs_start and lhs_start <= rhs_end


def parse(input_data):
    cubes = []
    for idx, line in enumerate(input_data.split("\n")):
        groups = re.search(r"(?P<sx>(\d+)),(?P<sy>(\d+)),(?P<sz>(\d+))~(?P<ex>(\d+)),(?P<ey>(\d+)),(?P<ez>(\d+))", line)
        sx, sy, sz, ex, ey, ez = (int(groups['sx']), int(groups['sy']), int(groups['sz']),
                                  int(groups['ex']), int(groups['ey']), int(groups['ez']))
        cubes.append(Cube(idx, (sx, sy, sz), (ex, ey, ez)))
    return cubes


def print_cubes(cubes):
    max_z = max(map(lambda c: c.sz, cubes)) + 2
    max_y = max(map(lambda c: c.sy, cubes)) + 1
    max_x = max(map(lambda c: c.sx, cubes)) + 1
    empty = '.'
    result_x = [[empty for _ in range(max_x)] for _ in range(max_z)]
    result_y = [[empty for _ in range(max_y)] for _ in range(max_z)]

    for cube in cubes:
        for z in range(cube.sz, cube.ez + 1):
            for x in range(cube.sx, cube.ex + 1):
                if result_x[z][x] == empty:
                    result_x[z][x] = cube.get_printable_id()
                else:
                    result_x[z][x] = '?'
            for y in range(cube.sy, cube.ey + 1):
                if result_y[z][y] == empty:
                    result_y[z][y] = cube.get_printable_id()
                else:
                    result_y[z][y] = '?'
    result_y[0] = ['-' for _ in range(max_y)]
    result_x[0] = ['-' for _ in range(max_x)]
    print('\n'.join([''.join(row) for row in reversed(result_x)]))
    print()
    print('\n'.join([''.join(row) for row in reversed(result_y)]))
    print()


def are_stable(cubes, min_z=1):
    for cube in cubes:
        if cube.sz <= min_z:
            continue
        if cube.can_fall(cubes):
            return False
    return True


def simulate_until_stable(cubes, min_z=1):
    while not are_stable(cubes, min_z):
        cubes = sorted(cubes)
        for i in tqdm(range(len(cubes))):
            cube = cubes[i]
            if cube.sz <= min_z:
                continue
            cubes[i] = cube.fall(cubes)
    return cubes


def part1(input_data, debug=False):
    cubes = parse(input_data)
    if debug: print_cubes(cubes)
    # fall
    print("Waiting for cubes to stabilize")
    cubes = simulate_until_stable(cubes)
    print("All cubes are stable")
    if debug: print_cubes(cubes)
    # check if cubes can be removed
    can_remove = 1
    for idx_to_omit in tqdm(range(len(cubes) - 1)):
        cube_to_omit = cubes[idx_to_omit]
        test_cubes = cubes[:idx_to_omit] + cubes[idx_to_omit + 1:]
        if are_stable(test_cubes, cube_to_omit.ez):
            # print(f"Can't remove {to_remove} because tower will fall")
            can_remove += 1
    return can_remove


def part2(input_data, debug=False):
    cubes = parse(input_data)
    if debug: print_cubes(cubes)
    # fall
    print("Waiting for cubes to stabilize")
    cubes = simulate_until_stable(cubes)
    print("All cubes are stable")
    if debug: print_cubes(cubes)
    # create cubes support graph
    graph = {cube.id: [] for cube in cubes}  # cube : [supported cubes]
    for cube in cubes:
        supporting = cube.get_supporting_cubes(cubes)
        for supp in supporting:
            graph[supp.id].append(cube.id)
    laying_on_ground = list(map(lambda c: c.id, filter(lambda c: c.sz == 1, cubes)))
    # count affected cubes with bfs from ground
    affected_counter = 0
    can_remove_counter = 0
    for removed in map(lambda c: c.id, cubes):
        visited = set()
        queue = deque(laying_on_ground)
        while len(queue) > 0:
            cube_id = queue.popleft()
            if cube_id in visited:
                continue
            visited.add(cube_id)
            if cube_id != removed:  # skip removed cube
                for neighbor in graph[cube_id]:
                    queue.append(neighbor)
        affected = len(cubes) - len(visited)
        if affected == 0:
            can_remove_counter += 1
        affected_counter += affected

    return affected_counter, can_remove_counter


def main():
    assert Cube(0, (1, 0, 1), (1, 2, 1)).collide(Cube(1, (0, 0, 1), (2, 0, 1))) is True
    assert Cube(0, (0, 0, 1), (2, 0, 1)).collide(Cube(2, (0, 2, 3), (2, 2, 3))) is False
    assert Cube(0, (0, 0, 10), (2, 0, 10)).fall([]) == Cube(0, (0, 0, 1), (2, 0, 1))
    assert Cube(0, (0, 0, 10), (2, 0, 10)).fall([Cube(2, (0, 0, 1), (2, 2, 1))]) == Cube(0, (0, 0, 2), (2, 0, 2))
    assert Cube(0, (0, 0, 4), (2, 0, 4)).can_fall([Cube(2, (0, 0, 3), (0, 2, 3))]) is False
    assert Cube(0, (0, 0, 4), (2, 0, 4)).can_fall([Cube(2, (0, 1, 4), (2, 1, 4))]) is True
    assert Cube(0, (0, 0, 4), (2, 0, 4)).can_fall([Cube(2, (0, 0, 3), (0, 0, 3))]) is False
    assert Cube(0, (0, 0, 14), (2, 0, 14)).fall([
        Cube(2, (0, 0, 2), (0, 0, 2))]) == Cube(0, (0, 0, 3), (2, 0, 3))
    assert Cube(0, (0, 0, 4), (0, 0, 4)).can_fall([Cube(2, (0, 1, 3), (0, 1, 3))]) is True
    assert Cube(0, (0, 0, 4), (0, 0, 4)).can_fall([
        Cube(2, (0, 1, 3), (0, 1, 3)),
        Cube(2, (1, 0, 3), (1, 0, 3)),
        Cube(2, (0, 0, 3), (0, 0, 3))
    ]) is False
    assert 5 == part1(puzzle.examples[0].input_data, True)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert (7, 5) == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    affected_counter, part2_can_remove = part2(puzzle.input_data)
    puzzle.answer_b = affected_counter
    print("part2 OK")


if __name__ == '__main__':
    main()
