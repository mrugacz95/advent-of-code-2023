from time import monotonic

from day01 import day01
from day02 import day02
from day03 import day03
from day04 import day04
from day05 import day05
from day06 import day06
from day07 import day07
from day08 import day08
from day09 import day09
from day10 import day10
from day11 import day11
from day12 import day12
from day13 import day13
from day14 import day14
from day15 import day15
from day16 import day16
from day17 import day17
from day18 import day18
from day19 import day19
from day20 import day20
from day21 import day21
from day22 import day22
from day23 import day23
from day24 import day24
from day25 import day25


def main():
    start_time = monotonic()
    day01.main()
    day02.main()
    day03.main()
    day04.main()
    day05.main()
    day06.main()
    day07.main()
    day08.main()
    day09.main()
    day10.main()
    day11.main()
    day12.main()
    day13.main()
    day14.main()
    day15.main()
    day16.main()
    day17.main()
    day18.main()
    day19.main()
    day20.main()
    day21.main()
    day22.main()
    day23.main()
    day24.main()
    day25.main()
    print(monotonic() - start_time, "seconds")


if __name__ == '__main__':
    main()
