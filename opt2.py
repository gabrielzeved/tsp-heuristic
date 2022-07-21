import main


def swap(tour, x, y):
    return tour[:x] + tour[x:y + 1][::-1] + tour[y + 1:]


def opt2(tour):
    stable, best = False, main.total_cost(tour)
    lengths, tours = [best], [tour]
    while not stable:
        stable = True
        for i in range(1, main.cities_len - 1):
            for j in range(i + 1, main.cities_len):
                candidate = swap(tour, i, j)
                length_candidate = main.total_cost(candidate)
                if best > length_candidate:
                    solution, best = candidate, length_candidate
                    tours.append(solution)
                    lengths.append(best)
                    stable = False
    return tours[-1]
