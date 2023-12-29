import abc
from collections import defaultdict, deque
from enum import Enum
from math import lcm

from aocd.models import Puzzle

puzzle = Puzzle(year=2023, day=20)


class State(Enum):
    LOW = 1
    HIGH = 2


PULSES_QUEUE = deque()


class Node(abc.ABC):
    def __init__(self, name):
        self.outputs = []
        self.inputs = []
        self.name = name

    def add_input(self, node):
        self.inputs.append(node)

    def add_output(self, node):
        self.outputs.append(node)

    @abc.abstractmethod
    def recv_pulse(self, sender_name, state):
        pass

    def send_pulse(self, state):
        for node in self.outputs:
            PULSES_QUEUE.append((self.name, state, node.name))


class BroadcastNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.outputs = []

    def recv_pulse(self, _, state):
        self.send_pulse(state)

    def __repr__(self):
        return f"{self.name} -> {','.join(map(lambda n: n.name, self.outputs))}"


class Conjunction(Node):

    def __init__(self, name):
        super().__init__(name)
        self.last_state = {}

    def add_input(self, node):
        super().add_input(node)
        self.last_state[node.name] = State.LOW

    def recv_pulse(self, sender_name, state):
        self.last_state[sender_name] = state
        if all(map(lambda x: x == State.HIGH, self.last_state.values())):
            self.send_pulse(State.LOW)
        else:
            self.send_pulse(State.HIGH)

    def __repr__(self):
        return f"&{self.name} -> {','.join(map(lambda n: n.name, self.outputs))}"


class FlipFlop(Node):
    OFF = 1
    ON = 2

    def __init__(self, name):
        super().__init__(name)
        self.state = FlipFlop.OFF

    def recv_pulse(self, sender_name, state):
        if state == State.HIGH:
            return
        if self.state == FlipFlop.ON:
            self.state = FlipFlop.OFF
            self.send_pulse(State.LOW)
        else:
            self.state = FlipFlop.ON
            self.send_pulse(State.HIGH)

    def __repr__(self):
        return f"%{self.name} -> {','.join(map(lambda n: n.name, self.outputs))}"


class TestNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.received = False

    def recv_pulse(self, sender_name, state):
        if state == State.LOW:
            self.received = True


def parse(input_data):
    graph = defaultdict(list)
    types = {}
    for line in input_data.split("\n"):
        node, next_nodes = line.split(" -> ")
        if node[0] in ['%', '&']:
            node_type, name = node[0], node[1:]
        elif node == 'broadcaster':
            node_type, name = 'b', node
        else:
            node_type, name = None, node
        types[name] = node_type
        for next_node in next_nodes.split(", "):
            graph[name].append(next_node)
            if next_node not in graph:  # add test nodes anyway
                graph[next_node] = []
                types[next_node] = None
    return graph, types


def connect_nodes(graph, types):
    nodes = {}
    for name, outputs in graph.items():
        node_type = types[name]
        if node_type == 'b':
            nodes[name] = BroadcastNode(name)
        elif node_type == '&':
            nodes[name] = Conjunction(name)
        elif node_type == '%':
            nodes[name] = FlipFlop(name)
        elif node_type is None:
            nodes[name] = TestNode(name)

    for name, outputs in graph.items():
        for output in outputs:
            nodes[name].add_output(nodes[output])
            nodes[output].add_input(nodes[name])
    return nodes


def part1(input_data):
    graph, types = parse(input_data)
    nodes = connect_nodes(graph, types)
    pulses = defaultdict(int)
    for i in range(1000):
        PULSES_QUEUE.append(('button', State.LOW, 'broadcaster'))
        while len(PULSES_QUEUE) > 0:
            sender_name, state, recv_name = PULSES_QUEUE.popleft()
            nodes[recv_name].recv_pulse(sender_name, state)
            # print(f"{sender_name} -{state}-> {recv_name}")
            pulses[state] += 1
    return pulses[State.HIGH] * pulses[State.LOW]


def part2(input_data):
    graph, types = parse(input_data)
    nodes = connect_nodes(graph, types)
    test_node: TestNode = nodes['rx']
    test_parent = test_node.inputs[0]
    cycles = {node.name: 0 for node in test_parent.inputs}

    def simulate():
        button_counter = 0
        while True:
            button_counter += 1
            PULSES_QUEUE.append(('button', State.LOW, 'broadcaster'))
            while len(PULSES_QUEUE) > 0:
                sender_name, state, recv_name = PULSES_QUEUE.popleft()
                nodes[recv_name].recv_pulse(sender_name, state)
                # print(f"{sender_name} -{state}-> {recv_name}")
                if state == State.HIGH and recv_name == test_parent.name:
                    if cycles[sender_name] == 0:
                        cycles[sender_name] = button_counter
                    if all(x > 0 for x in cycles.values()):
                        return

    simulate()
    return lcm(*cycles.values())


def main():
    assert 32000000 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    example = ("broadcaster -> a\n"
               "%a -> inv, con\n"
               "&inv -> b\n"
               "%b -> con\n"
               "&con -> output")
    assert 11687500 == part1(example)
    print("part1 test OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    example = ("broadcaster -> a1, a2\n"
               "%a1 -> b1\n"
               "%b1 -> c1\n"
               "%c1 -> d1\n"
               "%d1 -> e1\n"
               "%e1 -> con\n"
               "&con -> rx")

    assert 16 == part2(example)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
