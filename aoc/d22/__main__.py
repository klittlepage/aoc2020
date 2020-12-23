import aoc.d22.main as main

if __name__ == '__main__':
    with open('data/d22/example_02.txt', 'r', encoding='utf8') as input_file:
        next(input_file)
        next(input_file)
        next(input_file)

        main.p_2(input_file)
