import copy
import random
import main
import opt2


def restricted_candidate_list(greediness_value=0.5):
    sequence = [random.sample(list(range(0, main.cities_len)), 1)[0]]
    for i in range(0, main.cities_len):
        rand = random.random()
        if rand > greediness_value and len(sequence) < main.cities_len:
            unvisited = [x for x in main.all_cities_indexes if x not in sequence]
            next_city = main.nearest_neighbor(sequence[-1], unvisited)
            sequence.append(next_city)
        elif rand <= greediness_value and len(sequence) < main.cities_len:
            unvisited = [x for x in main.all_cities_indexes if x not in sequence]
            next_city = random.sample(unvisited, 1)[0]
            sequence.append(next_city)
    return sequence


def grasp(tour, iterations=50, rcl=25, greediness_value=0.5):
    count = 0
    best_solution = copy.deepcopy(tour)
    while count < iterations:
        # print('Iteration = ', count, ' Distance = ', main.total_cost(best_solution))
        rcl_list = []

        for i in range(0, rcl):
            rcl_list.append(restricted_candidate_list(greediness_value))
        candidate = int(random.sample(list(range(0, rcl)), 1)[0])
        tour = opt2.opt2(rcl_list[candidate])

        # é feito atualização utilizando busca local até encontrar um ponto de máximo local, ou seja enquanto o opt2 conseguir
        # fazer uma alteração na cadeia de cidades que melhore o resultado, o algoritmo continua
        while tour != rcl_list[candidate]:
            rcl_list[candidate] = copy.deepcopy(tour)
            tour = opt2.opt2(rcl_list[candidate])

        if main.total_cost(tour) < main.total_cost(best_solution):
            best_solution = copy.deepcopy(tour)
        count = count + 1
    return best_solution
