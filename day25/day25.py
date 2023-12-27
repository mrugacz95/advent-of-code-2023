import random
import sys
from collections import defaultdict, deque
from typing import Dict, List, Tuple

from aocd.models import Puzzle
from tqdm import tqdm

sys.setrecursionlimit(2000)
puzzle = Puzzle(year=2023, day=25)


def parse(input_data) -> Tuple[Dict[str, List[str]], List[Tuple[str, str]]]:
    graph = defaultdict(list)
    edges = []
    for line in input_data.split("\n"):
        source, neighbours = line.split(": ")
        for neighbour in neighbours.split(" "):
            graph[source].append(neighbour)
            graph[neighbour].append(source)
            edges.append((source, neighbour))
    return graph, edges


def get_graph_size(graph, start):
    visited = set()
    queue = deque([start])
    while len(queue) > 0:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            for neighbour in graph[vertex]:
                if neighbour not in visited:
                    queue.append(neighbour)
    return visited


def get_spanning_tree(graph):
    visited = set()
    queue = deque([graph.keys()[0]])
    tree = {}
    while len(queue) > 0:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            for neighbour in graph[vertex]:
                if neighbour not in visited:
                    tree[vertex].append(neighbour)
                    queue.append(neighbour)


def find_bridge(graph: Dict[str, List[str]]) -> List[Tuple[str, str]]:
    low = defaultdict()
    entry_time = {}
    visited = set()
    bridges = []
    time = 0

    def dfs(node, parent):
        nonlocal time
        visited.add(node)
        time += 1
        low[node] = time
        entry_time[node] = time
        for i, neighbour in enumerate(graph[node]):
            if neighbour == parent:
                continue
            if neighbour in visited:
                low[node] = min(low[node], entry_time[neighbour])
            else:
                dfs(neighbour, node)
                low[node] = min(low[node], low[neighbour])
                if low[neighbour] > entry_time[node]:
                    print(f'bridge is {node} -> {neighbour}')
                    bridges.append((node, neighbour))

    dfs(next(iter(graph.keys())), -1)
    return bridges


def part1_slow(input_data):
    graph, edges = parse(input_data)
    for i, (i1, i2) in enumerate(edges):
        for j, (j1, j2) in enumerate(edges[i + 1:]):
            for k1, k2 in edges[j + 1:]:
                if (i1, i2) == (j1, j2) or (j1, j2) == (k1, k2) or (i1, i2) == (k1, k2):
                    continue
                graph[i1].remove(i2)
                graph[i2].remove(i1)
                graph[j1].remove(j2)
                graph[j2].remove(j1)
                graph[k1].remove(k2)
                graph[k2].remove(k1)
                visited = set()
                cliques_sizes = []

                for vertex in graph:
                    if vertex not in visited:
                        clique = get_graph_size(graph, vertex)
                        visited.update(clique)
                        cliques_sizes.append(len(clique))
                if len(cliques_sizes) == 2:
                    print(f"Edges to remove: {i1}-{i2}, {j1}-{j2}, {k1}-{k2}")
                    return cliques_sizes[0] * cliques_sizes[1]

                graph[i1].append(i2)
                graph[i2].append(i1)
                graph[j1].append(j2)
                graph[j2].append(j1)
                graph[k1].append(k2)
                graph[k2].append(k1)


def part1_faster_but_still_slow(input_data):
    graph, edges = parse(input_data)
    progress = tqdm(total=(len(edges) * (len(edges) - 1)) // 2)
    for i, (i1, i2) in enumerate(edges):
        for j, (j1, j2) in enumerate(edges[i + 1:]):
            progress.update()
            if (i1, i2) == (j1, j2):
                continue
            graph[i1].remove(i2)
            graph[i2].remove(i1)
            graph[j1].remove(j2)
            graph[j2].remove(j1)

            bridges = find_bridge(graph)
            if len(bridges) == 1:
                k1, k2 = bridges[0]
                graph[k1].remove(k2)
                graph[k2].remove(k1)
                subgraph_size = len(get_graph_size(graph, next(iter(graph.keys()))))
                return subgraph_size * (len(graph) - subgraph_size)

            graph[i1].append(i2)
            graph[i2].append(i1)
            graph[j1].append(j2)
            graph[j2].append(j1)


def kargers_algorithm(input_graph):
    attempts = 0
    while True:
        graph = {k: v.copy() for k, v in input_graph.items()}
        joined = {v: {v} for v in graph.keys()}
        while len(graph) > 2:
            recipient = random.choice(list(graph.keys()))
            donor = random.choice(graph[recipient])
            # concat edge
            joined[recipient].update(joined[donor])
            del joined[donor]
            # unconnected recipient - donor
            graph[donor].remove(recipient)
            graph[recipient].remove(donor)
            # reconnect neighbours
            for neighbour in graph[donor]:
                graph[neighbour].append(recipient)
                graph[neighbour].remove(donor)
                graph[recipient].append(neighbour)
            # remove self cycles
            graph[recipient] = list(filter(lambda x: x != recipient, graph[recipient]))
            # remove donor node
            del graph[donor]
        attempts += 1
        # check if finished with 3 edges between two nodes
        if len(graph[list(graph.keys())[0]]) == 3 and len(joined) == 2:
            print(f"cut found after {attempts} attempts")
            s1, s2 = joined.keys()
            return len(joined[s1]) * len(joined[s2])


def part1(input_data):
    graph, edges = parse(input_data)
    return kargers_algorithm(graph)


def main():
    assert find_bridge({
        "a": ["b", "c", "d"],
        "b": ["a", "c", "d"],
        "c": ["a", "b", "d"],
        "d": ["a", "b", "c", "e"],
        "e": ["f", "g"],
        "f": ["e", "g"],
        "g": ["e", "f"]
    }) == [("d", "e")]
    example = ("jqt: rhn xhk nvd\n"
               "rsh: frs pzl lsr\n"
               "xhk: hfx\n"
               "cmg: qnr nvd lhk bvb\n"
               "rhn: xhk bvb hfx\n"
               "bvb: xhk hfx\n"
               "pzl: lsr hfx nvd\n"
               "qnr: nvd\n"
               "ntq: jqt hfx bvb xhk\n"
               "nvd: lhk\n"
               "lsr: lhk\n"
               "rzs: qnr cmg lsr rsh\n"
               "frs: qnr lhk lsr")

    assert 54 == part1_slow(example)
    assert 54 == part1_faster_but_still_slow(example)
    assert 54 == part1(example)

    assert 54 == part1(example)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")


if __name__ == '__main__':
    main()
