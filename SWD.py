from typing import List, Tuple, Set, Dict


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
    u = out2
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

    a = help_square(A1, A2, U[0])
    areas = {u: help_square(A1, A2, u) for u in U }
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


def main():
    points = [(0, 2), (1, 2), (1, 5), (2, 3), (2, 9), (3, 1), (3, 6), (3, 8), (4, 3), (4, 5), (4, 9), (5, 7), (6, 9), (6, 10), (7, 3), (7, 5), (7, 10), (8, 8), (9, 2), (9, 5), (9, 7), (9, 9), (10, 4), (10, 8), (10, 9), (11, 6), (11, 10), (12, 1), (12, 4), (12, 7)]
    limit = (len(points)//4) + 1
    sorting_points(points)
    A1, A2, U = divide_into_groups(points, limit)
    areas = field_of_square(A1, A2, U)
    areas = standardization_of_squares(areas)
    areas = ranking_creating(areas)
    # a = 1
    result = []
    for key, value in areas.items():
        elem = "{0}: {1}".format(key, [(val.a1,val.a2) for val in value])
        result.append(elem)
    print(result)


if __name__ == "__main__":
    main()

