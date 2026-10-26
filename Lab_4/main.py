from itertools import combinations

import numpy as np
from games import games
from scipy.optimize import linprog


def main():
    number = int(input("Enter the game number> "))
    game = games.get(number)
    if not game:
        print(f"Game {number} not found")
        return

    if len(game['players']) != 3:
        print(f"Incorect number of players: {game['players']}")
        return

    superaditivity = is_superaditivity(game)
    essentialy = is_essentialy(game)

    print(f'superaditivity: {superaditivity}')
    print(f'essentialy: {essentialy}')
    if not essentialy:
        return

    v_ = conversion_to_form_0_1(game)
    print('\n0-1 Form')
    print('\n'.join(
        f'{key}: {value}'
        for key, value in v_.items()
        if key != 'players'
    ))
    
    is_not_empty = c_core_is_not_empty(v_)
    print('\nC-core')
    print(f'C-core is not empty (100%): {is_not_empty}')

    print('\nDistribution')
    distribution = get_distribution(v_, game)
    if distribution is None:
        print('C-core is empty')
        return
    print(distribution)

    vector = shaply_vector(game)
    print('\nSheply Vector')
    print(vector)
    print(f'Belongs C-core: {vector_review(game, vector)}')

def is_superaditivity(g: dict) -> bool:
    players = g['players']
    for i in players:
        l = [p for p in players if p != i]
        if g[str(i)] + g[f'{l[0]}_{l[1]}'] > g['N']:
            return False
        for j in l:
            q, w = sorted([i, j])
            if g[str(i)] + g[str(j)] > g[f'{q}_{w}']:
                return False
    return True

def is_essentialy(g: dict) -> bool:
    sum_ = 0
    for i in g['players']:
        sum_ += g[str(i)]
    return sum_ < g['N']

def conversion_to_form_0_1(g: dict) -> dict:
    bottom = g['N'] - sum([g[str(i)] for i in g['players']])

    v_ = {str(i): 0 for i in g['players']}
    v_['N'] = 1
    v_['players'] = g['players']

    for key, value in g.items():
        if key not in v_:
            p = [int(i) for i in key.split('_')]
            sum_ = sum([g[str(i)] for i in p])
            v_[key] = (value - sum_) / bottom
    return v_

def c_core_is_not_empty(v_: dict) -> bool:
    n = len(v_['players'])
    for key, value in v_.items():
        if key != 'players':
            s = n if key == 'N' else len(key.split('_'))
            if value > 1 / (n - s + 1):
                return False
    return True

def get_distribution(v_: dict, g: dict) -> dict[int, float]:
    players = v_['players']
    n = len(players)

    A_ub = []
    b_ub = []

    for i in range(1, n):
        for coalition in combinations(players, i):
            key = '_'.join(map(str, coalition))
            value = v_[key]

            row = [
                -1 if p in coalition else 0
                for p in players
            ]

            A_ub.append(row)
            b_ub.append(-value)

    A_eq = [np.ones(n)]
    b_eq = [v_['N']]

    solve = linprog(
        c=np.zeros(n),
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(None, None)] * n,
        method='highs'
    )

    if not solve.success:
        return None

    d = {i: float(solve.x[i - 1]) for i in players}
    print(d)

    k_ = g['N'] - sum([g[str(i)] for i in players])
    d = {i: k_ * d[i] + g[str(i)] for i in players}

    return d

def shaply_vector(g: dict) -> dict:
    result = {}

    for i in g['players']:
        l = tuple(p for p in g['players'] if p != i)

        key_i_j = '_'.join(map(str, sorted((i, l[0]))))
        key_i_k = '_'.join(map(str, sorted((i, l[1]))))
        key_j_k = '_'.join(map(str, sorted(l)))

        sum_ = (1 / 3) * g[str(i)]

        sum_ += (1 / 6) * ( (g[key_i_j] - g[str(l[0])]) + (g[key_i_k] - g[str(l[1])]) )

        sum_ += (1 / 3) * (g['N'] - g[key_j_k])
        result[i] = sum_

    return result

def vector_review(g: dict, vector: dict) -> bool:
    players = g['players']

    if sum(vector[i] for i in players) != g['N']:
        return False

    for i in range(1, len(players)):
        for s in combinations(players, i):
            key = '_'.join(map(str, s))
            if sum(vector[i] for i in s) < g[key]:
                return False
    return True

if __name__ == "__main__":
    main()
