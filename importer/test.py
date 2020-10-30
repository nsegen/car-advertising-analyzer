import itertools
import operator

values = [(1, 'Order Status'), (2, 'BoP Execution'), (4, 'QG'), (8, 'Kitting'), (16, 'Replacement')]
combinations = [
    *itertools.combinations(values, 1),
    *itertools.combinations(values, 2),
    *itertools.combinations(values, 3), 
    *itertools.combinations(values, 4), 
    *itertools.combinations(values, 5),
]

def get_binary_mask(chain):
    mask = 0
    string_mask = []

    for val in chain:
        mask = mask | val[0]
        string_mask.append(val[1])
    return mask, ' + '.join(string_mask)

formatted_combinations = [get_binary_mask(comb) for comb in combinations]
sorted_combinations = sorted(formatted_combinations, key=operator.itemgetter(0))

for comb in sorted_combinations:
    print(f"when {comb[0]} then '{comb[1]}'")


