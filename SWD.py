from typing import List, Tuple, Set, Dict
import numpy as np


class Areas:
    """
    Klasa służaca do obrazowania relacji (pole jakie tworzą punkty)
    między dwoma zbiorami: A1 i A2
    """
    def __init__(self, a1, a2, area):
        self.a1 = a1
        self.a2 = a2
        self.area = area


def sorting_points(points: List[Tuple[int]]) -> List[Tuple[int]]:
    """
    Sortowanie punktów w zależności od odległości od punktu (0,0)
    """
    return sorted(points, key=lambda x: (x[0] ** 2 + x[1] ** 2) ** 0.5)


def divide_into_groups(points: List[Tuple[int]], limit: int) -> Tuple[List[Tuple[int]]]:
    considered_points = points[limit:-limit]
    #ograniczenie zbiorów a następnie podzielenie ich
    candidates_a1 = considered_points[:len(considered_points)//2]
    candidates_a2 = considered_points[len(considered_points)//2:]

    out1 = check_if_points_independant(candidates_a1)
    #usuniecie punktow zaleznych z a1
    a1 = [i for i in candidates_a1 if i not in out1]
    out2 = check_if_points_independant(candidates_a2)
    u = out1
    #usuniecie punktow zaleznych z a2
    a2 = [i for i in candidates_a2 if i not in out2]
    return a1, a2, u


def check_if_points_independant(points: List[Tuple[int]]):
    # funkcja sprawdzająca  kolejny punkt po punkcie czy kazdy z nich jets punktem nie zaleznym w danym podzbiorze
    index = []
    for i in points:
        for j in points:
            if i[0] <= j[0] and i[1] <= j[1] and j not in index and i != j:
                index.append(j)
            elif i[0] >= j[0] and i[1] >= j[1] and i not in index and i != j:
                index.append(i)
    return index


def field_of_square(A1: List[Tuple[int]], A2: List[Tuple[int]], U: List[Tuple[int]]) -> Dict[Tuple[int], List[object]]:
    """
    funkcja licząca pola dla wyznaczonych kwadratów w zależności od danego U
    """
    def help_square(A1: List[Tuple[int]], A2: List[Tuple[int]], u: Tuple[int]) -> List[object]:
        """
        Funkcja pomocnicza, liczy pola dla konkretnego, jednego u
        """
        areas = []
        for a1 in A1:
            for a2 in A2:
                area = abs(max(a2[1], a1[1], u[1]) - min(a2[1], a1[1], u[1])) * abs(max(a2[0], a1[0], u[0]) - min(a2[0], a1[0], u[0]))
                areas.append(Areas(a1, a2, area))
        return areas
    A1_x = [i[0] for i in A1]
    A1_y = [i[1] for i in A1]
    A2_x = [i[0] for i in A2]
    A2_y = [i[1] for i in A2]
    a = help_square(A1, A2, U[0])
    areas = {u: help_square(A1, A2, u) for u in U if u[0] >= min(A1_x) and u[1] >= min(A1_y) and u[0] <= max(A2_x) and u[1] <= max(A2_y)}
    return areas


def standardization_of_squares(areas: Dict[Tuple[int], List[object]]) -> Dict[Tuple[int], List[object]]:
    """
    Funkcja standaryzująca pola kwadratow
    """
    # utworzenie słownika pomocniczego klucz: u, wartość to suma pól dla danego u
    help_sum = {}
    for k, val in areas.items():
        temp = [v.area for v in val]
        help_sum[k] = sum(temp)

    # uaktualnienie głównego słownika (standaryzacja)
    for keys, values in areas.items():
        for val in values:
            val.area = val.area/help_sum[keys]
    return areas


def ranking_creating(areas: Dict[Tuple[int], List[object]]) -> Dict[Tuple[int], List[object]]:
    """
    Posortowanie słownika klucz: u, wartość: lista punktów
    tworząca pola wokół punktu u w zależności rosnącej względem pola kwadratu (area)
    """
    for keys, values in areas.items():
        values.sort(key=lambda x: x.area)
    return areas


def calc_weights(areas: Dict[Tuple[int], List[object]]) -> Dict[Tuple[int], List[float]]:

    '''
    Funkcja licząca wagi dla każdego punktu u
    Zwraca słownik {punkt u: lista wag}
    '''

    weights: Dict[Tuple[int], List[float]] = {}

    for u, fields in areas.items():
        list_of_fields = [A.area for A in fields]
        sum_of_fields = sum(list_of_fields)
        weights_for_one_u = []

        for A in fields:
            weights_for_one_u.append(A.area/sum_of_fields)

        weights[u] = weights_for_one_u

    return weights


def calc_distance_coefficients(areas: Dict[Tuple[int], List[object]]) -> Dict[Tuple[int], List[float]]:

    '''
    Funkcja licząca współczynniki odległości dla każdego punktu u
    Zwraca słownik {punkt u: lista współczynników}
    '''

    distance_coefs: Dict[Tuple[int], List[float]] = {}

    for u, fields in areas.items():
        distance_coefs_for_one_u = []

        for A in fields:
            u_ = np.array([u[0], u[1]])
            a1 = np.array([A.a1[0], A.a1[1]])
            a2 = np.array([A.a2[0], A.a2[1]])
            d1 = np.linalg.norm(u_ - a1)
            d2 = np.linalg.norm(u_ - a2)
            if d1 > d2:
                distance_coefs_for_one_u.append(d1/(d1 + d2))
            else:
                distance_coefs_for_one_u.append(d2/(d1 + d2))

        distance_coefs[u] = distance_coefs_for_one_u

    return distance_coefs

def calc_score_function(weights: Dict[Tuple[int], List[float]], distance_coefs: Dict[Tuple[int], List[float]]) ->  Dict[Tuple[int], float]:

    '''
    Funkcja licząca wartości scoringowe dla każdego punktu u
    Zwraca słownik {punkt u: wartość scoringowa}
    '''

    ranking:  Dict[Tuple[int], float] = {}

    for u in weights:
        w = np.array(weights[u])
        d = np.array(distance_coefs[u])
        ranking[u] = w@d.T

    ranking = {u: value for u, value in sorted(ranking.items(), key=lambda item: item[1])}

    return ranking


def main():
    points = [(0, 2), (1, 2), (1, 5), (2, 3), (2, 9), (3, 1), (3, 6), (3, 8), (4, 3), (4, 5), (3, 6), (5, 7), (6, 9), (6, 10), (5, 3), (7, 5), (7, 10), (8, 8), (9, 2), (9, 5), (9, 7), (9, 9), (10, 4), (10, 8), (10, 9), (11, 6), (11, 10), (12, 1), (12, 4), (12, 7)]
    #points = [(0, 2), (1, 2), (1, 5), (2, 3), (2, 9), (3, 1), (3, 6), (3, 8), (4, 3), (4, 5), (4, 9), (5, 7), (6, 9), (6, 10), (7, 3), (7, 5), (7, 10), (8, 8), (9, 2), (9, 5), (9, 7), (9, 9), (10, 4), (10, 8), (10, 9), (11, 6), (11, 10), (12, 1), (12, 4), (12, 7)]
    limit = (len(points)//4) + 1
    sorting_points(points)
    A1, A2, U = divide_into_groups(points, limit)
    areas = field_of_square(A1, A2, U)
    weights = calc_weights(areas)
    distance_coefs = calc_distance_coefficients(areas)
    ranking = calc_score_function(weights, distance_coefs)

    print(ranking)



if __name__ == "__main__":
    main()