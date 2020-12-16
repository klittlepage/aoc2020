import aoc.d15.main as main

if __name__ == '__main__':
    with open('data/d15/example_01.txt', 'r', encoding='utf8') as input_file:
        next(input_file)
        next(input_file)
        next(input_file)
        main.p_1(input_file)
