import re
from functools import cache
from itertools import islice

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=12)

DEBUG = False


def parse(input_data):
    lines = []
    for line in input_data.split("\n"):
        springs, groups = line.split(" ")
        groups = list(map(int, groups.split(",")))
        lines.append((springs, groups))
    return lines


def correct_arrangement(springs, groups):
    assert '?' not in springs
    spings_groups = re.split(r"\.+", springs.strip('.'))
    return groups == list(map(lambda x: len(x), spings_groups))


def fill_springs(spring, pattern):
    filled = spring
    used = 0
    for i, c in enumerate(filled):
        if c == '?':
            filled = filled[:i] + pattern[used] + filled[i + 1:]
            used += 1
            if used == len(pattern):
                break
    return filled


def generate_patterns(hash_left, dot_left, acc):
    if hash_left == 0 and dot_left == 0:
        yield acc
    if hash_left > 0:
        for pattern in generate_patterns(hash_left - 1, dot_left, acc + "#"):
            yield pattern
    if dot_left > 0:
        for pattern in generate_patterns(hash_left, dot_left - 1, acc + "."):
            yield pattern


def part1(input_data):
    data = parse(input_data)
    all_possibilities = 0
    for spring, groups in data:
        unknown_symbols = sum(map(lambda x: x == '?', spring))
        known_hash_symbols = sum(map(lambda x: x == '#', spring))
        unknown_hash_symbols = sum(groups) - known_hash_symbols
        unknown_dot_symbols = unknown_symbols - unknown_hash_symbols
        possible_ways = 0
        for pattern in generate_patterns(unknown_hash_symbols, unknown_dot_symbols, ""):
            filled = fill_springs(spring, pattern)
            if correct_arrangement(filled, groups):
                possible_ways += 1
        if DEBUG: print(spring, possible_ways)
        all_possibilities += possible_ways
    return all_possibilities


def window(seq, n):
    """
    Source https://stackoverflow.com/a/6822773/5342020
    Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ..."""
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def can_group_start(pattern, group_len):
    if '.' not in pattern[:group_len] and (len(pattern) == group_len or pattern[group_len] in ['?', '.']):
        return True
    return False


@cache
def count_possibilities(spring, groups):
    if len(groups) == 0 and "#" not in spring:
        if DEBUG: print("possible", spring, groups)
        return 1
    if len(groups) == 0:
        if DEBUG: print("impossible", spring, groups)
        return 0
    if DEBUG: print(spring, groups)
    possibilities = 0
    group_len = groups[0]
    # find every suffix and check if group can start from it
    for start_pos in range(len(spring)):
        sufix = spring[start_pos:]
        if len(sufix) < group_len:  # optimisation
            break
        if can_group_start(sufix, group_len):
            if DEBUG:
                print('next call from', spring, group_len, "pos", start_pos, "sufix:",
                      sufix[group_len + 1:], "new groups", groups[1:])
            # check if suffix will match remaining groups
            possibilities += count_possibilities(sufix[group_len + 1:], groups[1:])
        if spring[start_pos] == '#':  # must use all hash symbols
            if DEBUG: print("must use # at pos ", start_pos)
            break
    if DEBUG: print("result", possibilities)
    return possibilities


def part2(input_data):
    data = parse(input_data)
    for idx, (spring, groups) in enumerate(data):
        new_spring = '?'.join(spring for _ in range(5))
        data[idx] = new_spring, groups * 5
    all_possibilities = 0
    for spring, groups in data:
        possibilities = count_possibilities(spring, tuple(groups))
        if DEBUG: print(possibilities)
        all_possibilities += possibilities
    return all_possibilities


def main():
    example_part1 = ("???.### 1,1,3\n"
                     ".??..??...?##. 1,1,3\n"
                     "?#?#?#?#?#?#?#? 1,3,1,6\n"
                     "????.#...#... 4,1,1\n"
                     "????.######..#####. 1,6,5\n"
                     "?###???????? 3,2,1")
    assert list(generate_patterns(2, 1, "")) == ["##.", "#.#", ".##"]
    assert correct_arrangement("..#..#....###.", [1, 1, 3])
    assert correct_arrangement(".#.###.#.######", [1, 3, 1, 6])
    assert 1 == part1("?#?#?#?#?#?#?#? 1,3,1,6")
    assert 21 == part1(example_part1)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert can_group_start("#...", 1)
    assert can_group_start("#", 1)
    assert not can_group_start("...#", 1)
    assert can_group_start("#.#", 1)
    assert can_group_start("?.#", 1)
    assert can_group_start("#....", 1)
    assert can_group_start("###..#.#.", 3)
    assert can_group_start("#??##", 5)
    assert not can_group_start(".#####", 5)
    assert not can_group_start("???.######..#####.", 6)
    assert not can_group_start("?#??#", 1)

    assert count_possibilities("#", (1,)) == 1
    assert count_possibilities("#.#", (1, 1,)) == 1
    assert count_possibilities("#.?", (1, 1,)) == 1
    assert count_possibilities("#.?#.#", (1, 2, 1,)) == 1
    assert count_possibilities("????.######..#####.", (1, 6, 5,)) == 4
    assert count_possibilities("?#?#?#?#?#?#?#?", (1, 3, 1, 6)) == 1
    assert count_possibilities("?#??#", (1, 1)) == 1
    assert count_possibilities("#??#??#", (1, 1, 1)) == 1
    assert count_possibilities("?#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#?",
                               (1, 3, 1, 6, 1, 3, 1, 6, 1, 3, 1, 6, 1, 3, 1, 6, 1, 3, 1, 6)) == 1

    assert 1 == part2("???.### 1,1,3")
    assert 16384 == part2(".??..??...?##. 1,1,3")
    assert 1 == part2("?#?#?#?#?#?#?#? 1,3,1,6")
    assert 16 == part2("????.#...#... 4,1,1")
    assert 2500 == part2("????.######..#####. 1,6,5")
    assert 506250 == part2("?###???????? 3,2,1")

    print("part2 tests OK")
    assert 525152 == part2(example_part1)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
