import math
import re
from math import isnan

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=19)


def parse(input_data):
    # Sample: px{a<2006:qkq,m>2090:A,rfg}
    workflows, items = input_data.split("\n\n")
    result_workflows = {}
    for workflow in workflows.split("\n"):
        name, rules = workflow.split("{")
        rules = rules[:-1]
        result_rules = []
        for rule in rules.split(','):
            if ':' in rule:
                condition, next_name = rule.split(":")
                attr = condition[0]
                op = condition[1]
                value = int(condition[2:])
                result_rules.append((attr, op, value, next_name))
            else:
                result_rules.append((None, None, None, rule))
        result_workflows[name] = result_rules
    items = items.split("\n")
    result_items = []
    for item in items:
        group = re.search(r"{x=(?P<x>([0-9]+)),m=(?P<m>([0-9]+)),a=(?P<a>([0-9]+)),s=(?P<s>([0-9]+))}", item)
        result_items.append({
            'x': int(group['x']),
            'm': int(group['m']),
            'a': int(group['a']),
            's': int(group['s']),
        })
    return result_workflows, result_items


def apply_rule(item, rule):
    attr, op, value, next_name = rule
    if attr is None:
        return next_name
    else:
        lt = (lambda x: x[0] < x[1])
        gt = (lambda x: x[0] > x[1])
        op = lt if op == '<' else gt
        return next_name if op((item[attr], value)) else None


def part1(input_data):
    workflows, items = parse(input_data)
    accepted_items = []
    for item in items:
        workflow = 'in'
        while workflow != 'A' and workflow != 'R':
            for rule in workflows[workflow]:
                next_workflow = apply_rule(item, rule)
                if next_workflow is not None:
                    workflow = next_workflow
                    break
        if workflow == 'A':
            accepted_items.append(item)
    result_sum = 0
    for item in accepted_items:
        for value in item.values():
            result_sum += value
    return result_sum


class Range:
    def __init__(self, start=-float('inf'), end=float('inf')):
        self.start = start
        self.end = end

    def __add__(self, other):
        if self._overlap(other):
            return Range(max(self.start, other.start), min(self.end, other.end))
        else:
            return Range.empty()

    def _overlap(self, other):
        return self.end >= other.start and self.start <= other.end

    def __repr__(self):
        return f'({self.start}; {self.end})'

    def __copy__(self):
        return Range(self.start, self.end)

    def invert(self):
        if math.isinf(self.start):
            return Range(self.end + 1, float('inf'))
        if math.isinf(self.end):
            return Range(-float('inf'), self.start - 1)

    def is_empty(self):
        return isnan(self.start)

    def __len__(self):
        return self.end - self.start + 1

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    @staticmethod
    def from_rule(op, value):
        if op is None:
            return Range.full()  # full range
        if op == '>':
            return Range(start=value + 1)
        else:
            return Range(end=value - 1)

    @staticmethod
    def empty():
        return Range(float('nan'), float('nan'))

    @staticmethod
    def full():
        return Range(-float('inf'), float('inf'))


def convert_to_graph(workflows):
    queue = [('in', 0)]
    graph = {}  # (workflow, # of rule in workflow) : (category, left range, left node, right range, right node)
    visited = {('A', 0), ('R', 0)}
    while len(queue) > 0:
        name, node_id = queue.pop(0)
        if (name, node_id) in visited:
            continue
        visited.add((name, node_id))
        attr, op, value, next_name = workflows[name][node_id]
        if attr is None:
            graph[(name, node_id)] = (None, Range.empty(), (next_name, 0), Range.empty(), None)
        else:
            rule = Range.from_rule(op, value)
            graph[(name, node_id)] = (attr, rule, (next_name, 0),
                                      rule.invert(), (name, node_id + 1))

        if attr is not None:
            queue.append((name, node_id + 1))
        queue.append((next_name, 0))
    return graph


def part2(input_data):
    workflows, _ = parse(input_data)
    graph = convert_to_graph(workflows)
    xmas = {
        x: Range(1, 4000) for x in 'xmas'
    }
    visited = {('A', 0), ('R', 0)}
    possible_ranges = []

    def dfs(node, xmas_range):
        node_name, _ = node
        if node_name == 'A':
            possible_ranges.append(xmas_range)
            return
        if node in visited:
            return
        visited.add(node)
        attr, left_range, left_node, right_range, right_node = graph[node]

        if attr is not None:
            # in range
            new_ranges = xmas_range.copy()
            new_ranges[attr] = xmas_range[attr] + left_range
            if all([not r.is_empty() for r in new_ranges.values()]):
                dfs(left_node, new_ranges)
            # out of range
            new_ranges = xmas_range.copy()
            new_ranges[attr] = xmas_range[attr] + right_range
            if all([not r.is_empty() for r in new_ranges.values()]):
                dfs(right_node, new_ranges)
        else:  # next node without rule
            dfs(left_node, xmas_range)
        visited.remove(node)

    dfs(('in', 0), xmas)
    result = 0
    for possible in possible_ranges:
        current_possible = 1
        for possible_range in possible.values():
            current_possible *= len(possible_range)
        result += current_possible
    return result


def main():
    assert 19114 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert Range(1, 5) + Range(3, 10) == Range(3, 5)
    assert Range(-float('inf'), 5).invert() == Range(6, float('inf'))
    assert Range(6, float('inf')).invert() == Range(-float('inf'), 5)
    assert Range(1, 2).__len__() == 2

    assert 167409079868000 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
