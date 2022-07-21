from random import randrange, randint, sample, random
from numpy.random import choice
import numpy as np

import main


def swap_mutation(tour):
    i, j = randrange(len(tour)), randrange(len(tour))
    tour[i], tour[j] = tour[j], tour[i]
    return tour


def crossover_cut(size):
    first_cut = randint(1, size - 2)
    return first_cut, randint(first_cut + 1, size)


def order_crossover(i1, i2):
    a, b = crossover_cut(main.cities_len)
    ni1, ni2, i1, i2 = i1[a:b], i2[a:b], i1[b:] + i1[:b], i2[b:] + i2[:b]
    for x in i1:
        if x in ni2:
            continue
        ni2.append(x)
    for x in i2:
        if x in ni1:
            continue
        ni1.append(x)
    return ni1, ni2


def selection(generation, size=None):
    if size is None:
        size = len(generation)

    fitness_results = []
    for i in range(0, size):
        fitness_results.append(main.total_cost(generation[i]))

    sum_fitness = sum(fitness_results)
    probability_lst = [f / sum_fitness for f in fitness_results]

    np_gen = np.array(generation[:size])
    rnd_indices = np.random.choice(len(np_gen), size=size, p=probability_lst)

    mating_pool = np_gen[rnd_indices]

    return mating_pool.tolist()


def new_generation(greediness_value=0.5):
    sequence = [sample(list(range(0, main.cities_len)), 1)[0]]

    for i in range(0, main.cities_len):
        rand = random()
        if rand > greediness_value and len(sequence) < main.cities_len:
            unvisited = [x for x in main.all_cities_indexes if x not in sequence]
            next_city = main.nearest_neighbor(sequence[-1], unvisited)
            sequence.append(next_city)
        elif rand <= greediness_value and len(sequence) < main.cities_len:
            unvisited = [x for x in main.all_cities_indexes if x not in sequence]
            next_city = sample(unvisited, 1)[0]
            sequence.append(next_city)
    return sequence


def fill_generation(generation):
    # we select using the roulette wheel technique and keep only the best n elements
    if generation:
        generation = selection(generation, 40)
    while len(generation) < 70:
        generation.append(new_generation())
    return generation


def cycle(generation, crossover_rate=0.8, mutation_rate=0.1):
    ng = fill_generation(generation)

    for par in zip(generation[::2], generation[1::2]):
        ng.extend(order_crossover(*par) if random() < crossover_rate else par)

    ng = [swap_mutation(i) if random() < mutation_rate else i for i in ng]

    ng = sorted(ng, key=main.total_cost)
    return ng, ng[0]
