import re
from typing import List

from aocd.models import Puzzle
from tqdm import tqdm

puzzle = Puzzle(year=2023, day=5)


def parse(data_input):
    def parse_mappings(loc_mappings):
        parsed = []
        for line in loc_mappings.split("\n")[1:]:
            parsed.append(list(map(int, line.split(" "))))
        return parsed

    lines = data_input.split("\n\n")
    seeds = list(map(int, re.findall("[0-9]+", lines[0][6:])))
    seed2soil = parse_mappings(lines[1])
    soil2fertilizer = parse_mappings(lines[2])
    fertilizer2water = parse_mappings(lines[3])
    water2light = parse_mappings(lines[4])
    light2temp = parse_mappings(lines[5])
    temp2humidity = parse_mappings(lines[6])
    humidity2location = parse_mappings(lines[7])
    return (seeds, [seed2soil, soil2fertilizer, fertilizer2water,
                    water2light, light2temp, temp2humidity, humidity2location])


def find_mapping(value, mapping):
    for idx, value_range in enumerate(mapping):
        if value_range[1] <= value < value_range[1] + value_range[2]:
            diff = value - value_range[1]
            return value_range[0] + diff
    return value


def find_location(seed, mappings):
    seed2soil, soil2fertilizer, fertilizer2water, water2light, light2temp, temp2humidity, humidity2location = mappings
    soil = find_mapping(seed, seed2soil)
    fertilizer = find_mapping(soil, soil2fertilizer)
    water = find_mapping(fertilizer, fertilizer2water)
    light = find_mapping(water, water2light)
    temp = find_mapping(light, light2temp)
    humidity = find_mapping(temp, temp2humidity)
    location = find_mapping(humidity, humidity2location)
    return location


def part1(input_data):
    (seeds, mappings) = parse(input_data)
    locations = []
    for seed in seeds:
        locations.append(find_location(seed, mappings))
    return min(locations)


def reverse_mappings(mappings: List[List[List[int]]]):
    new_mapping = []
    for mapping in mappings:
        new_range = []
        for value_range in mapping:
            new_range.append((value_range[1], value_range[0], value_range[2]))
        new_mapping.append(new_range)
    return new_mapping


class Range:
    def __init__(self):
        self.ranges = []

    def add_range(self, range_from, range_to):
        self.ranges.append((range_from, range_to))

    def contains(self, value):
        for range_from, range_to in self.ranges:
            if range_from <= value < range_to:
                return True
        return False


def find_seed(location, mappings):
    soil2seed, fertilizer2soil, water2fertilizer, light2water, temp2light, humidity2temp, location2humidity = mappings
    humidity = find_mapping(location, location2humidity)
    temp = find_mapping(humidity, humidity2temp)
    light = find_mapping(temp, temp2light)
    water = find_mapping(light, light2water)
    fertilizer = find_mapping(water, water2fertilizer)
    soil = find_mapping(fertilizer, fertilizer2soil)
    seed = find_mapping(soil, soil2seed)
    return seed


def part2(input_data):
    progress = tqdm()
    (seeds, mappings) = parse(input_data)
    mappings = reverse_mappings(mappings)
    location = 0
    seeds_range = Range()
    for idx in range(0, len(seeds), 2):
        seeds_range.add_range(seeds[idx], seeds[idx] + seeds[idx + 1])
    while True:
        seed = find_seed(location, mappings)
        if seeds_range.contains(seed):
            progress.clear()
            return location
        location += 1
        if location % 500_000 == 0:
            progress.update(location)
        if location > 1_000_000_000:
            raise RuntimeError("Location not found :(")


def main():
    assert 35 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 46 == part2(puzzle.examples[0].input_data)
    print("\npart2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("\npart2 OK")


if __name__ == '__main__':
    main()
