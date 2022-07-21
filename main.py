import math

import genetic_algorithm
import grasp
import opt2

import time

filename = "data/p01_d.txt"


def load_matrix():
    matrix = open(filename).read()
    matrix = [item.split() for item in matrix.split('\n')[:-1]]
    matrix = [[int(num) for num in line] for line in matrix]
    return matrix


def set_diagonal(matrix):
    for i in range(0, len(matrix)):
        matrix[i][i] = math.inf


data = load_matrix()
set_diagonal(data)

cities_len = len(data[0])
all_cities_indexes = list(range(0, cities_len))


def nearest_neighbor_build():
    start_node = 0
    current_node = start_node
    tour = [current_node]

    unvisited = [x for x in all_cities_indexes if x not in tour]

    while unvisited:
        current_node = nearest_neighbor(current_node, unvisited)
        tour.append(current_node)
        unvisited.remove(current_node)
    return tour


def nearest_neighbor(current_node, unvisited_list):
    return min(unvisited_list, key=lambda x: data[x][current_node])


def total_cost(tour):
    total = 0
    for x in range(len(tour) - 1):
        total += data[tour[x]][tour[x + 1]]
    total += data[tour[-1]][tour[0]]
    return total


def distance_in_between(i, j, k):
    return data[i][k] + data[k][j] - data[i][j]


def add_closest_to_tour(tour):
    best_dist, new_tour = math.inf, None
    for city in range(0, cities_len):
        if city in tour:
            continue

        for index in range(len(tour) - 1):
            dist = distance_in_between(tour[index], tour[index + 1], city)
            if dist < best_dist:
                best_dist = dist
                new_tour = tour[:index + 1] + [city] + tour[index + 1:]
    return best_dist, new_tour


def cheapest_insertion_build():
    start_node = 0
    current_node = start_node

    tour = [current_node]
    unvisited = [x for x in all_cities_indexes if x not in tour]

    neighbor = nearest_neighbor(current_node, unvisited)
    tour.append(neighbor)

    while unvisited:
        _, tour = add_closest_to_tour(tour)
        unvisited = [x for x in all_cities_indexes if x not in tour]
    return tour


def opt2_iter(tour):
    old_tour = None
    count = 0
    while tour != old_tour:
        count += 1
        old_tour = tour
        tour = opt2.opt2(tour)
    return tour


if __name__ == '__main__':

    print(cities_len)

    start_time = time.time()
    nearest_neighbor_tour = nearest_neighbor_build()
    print('NN: ', total_cost(nearest_neighbor_tour))
    print('Execution Time: ', (time.time() - start_time))

    start_time = time.time()
    cheapest_insertion_tour = cheapest_insertion_build()
    print('CI: ', total_cost(cheapest_insertion_tour))
    print('Execution Time: ', (time.time() - start_time))

    start_time = time.time()
    opt2_tour = opt2_iter(cheapest_insertion_tour)
    print('OPT2: ', total_cost(opt2_tour))
    print('Execution Time: ', (time.time() - start_time))

    start_time = time.time()
    grasp_tour = grasp.grasp(cheapest_insertion_tour)
    print('GRASP: ', total_cost(grasp_tour))
    print('Execution Time: ', (time.time() - start_time))

    start_time = time.time()
    cycles = 200
    generation = genetic_algorithm.fill_generation([])
    for it in range(0, cycles):
        generation, best = genetic_algorithm.cycle(generation)
    print('GA: ', total_cost(best))
    print('Execution Time: ', (time.time() - start_time))

