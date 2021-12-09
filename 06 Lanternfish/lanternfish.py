# https://adventofcode.com/2021/day/6

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    initial_population = [int(i) for i in file.read().split(',')]


def growth_sim(days, init_pop):
    fish_pop = {}
    for i in range(9):
        fish_pop.setdefault(i, 0)
    for fish in init_pop:
        fish_pop[fish] += 1
    for i in range(days):
        fish_pop_new = {}
        for i in range(9):
            if i == 8:
                fish_pop_new[i] = fish_pop[0]
            elif i == 6:
                fish_pop_new[i] = fish_pop[i+1] + fish_pop[0]
            else:
                fish_pop_new[i] = fish_pop[i+1]
        fish_pop = fish_pop_new
    print(f"Population after {days} days: {sum(fish_pop.values())}")


growth_sim(80, initial_population)  # Part 1

growth_sim(256, initial_population)  # Part 2
