from typing import List, Tuple, Set, Dict

class Areas:
    '''
    Klasa służaca do obrazowania relacji (pole jakie tworzą punkty)
    między dwoma zbiorami: A1 i A2
    '''
    def __init__(self, a1, a2, area):
        self.a1 = a1
        self.a2 = a2
        self.area = area

def sorting_points(points: List[Tuple[int]]) -> List[Tuple[int]]:
    '''
    Sortowanie punktów w zależności od odległości od punktu (0,0)
    '''

    # ułożenie punktów w liście w zależności od odpegłości od punktu (0,0)
    # sortowanie bąbelkowe
    for i in range(len(points)-1):
        for j in range(len(points)-i-1):
            if points[j][0]**2 + points[j][1]**2 > points[j+1][0]**2 + points[j+1][1]**2:
                temp = points[j]
                points[j] = points[j+1]
                points[j+1] = temp
    return points

def divide_into_groups(points: List[Tuple[int]], limit: int) -> Tuple[List[Tuple[int]]]:

    '''
    Funkcja wyznacza zbiory A1, A2, punkty u, zakładając konkretną ilość 
    punktów idealnych i punktów nadiru
    '''

    def help_divide(points: List[Tuple[int]]) -> List[Tuple[int]]:
        '''
        Sam proces sparwdzania niezależności punktów
        '''
        considered = points[0]
        set_a = [points]

        # wyszukiwanie punktow niezależnych względem pierwszego wybranego punktu
        while len(set_a) == 1:
            set_a = [considered]
            for point in points[1:]:
                if (point[0] > considered[0]) ^ (point[1] > considered[1]):
                    set_a.append(point)
            points = points[1:]
            considered = points[0]

        set_better = [set_a[0]]

        # eliminacja punktów spośród potencjalnych należących do zbioru,
        #  jeśli jedna ze współrzędnych się pokrywa
        for a_elem in set_a[1:]:
            choice = True
            for b_elem in set_better:
                if a_elem[0] == b_elem[0] or a_elem[1] == b_elem[1]:
                    choice = False
                if a_elem[0] == b_elem[1] or a_elem[1] == b_elem[0]:
                    choice = False
            if choice:
                set_better.append(a_elem)

        return set_better

    # podział punktów na grupy: idealne, antyidealne i rozpatrywane
    # ideal_points = points[:limit]
    # nadir_points = points[-limit:]
    considered_points = points[limit:-limit]

    candidates_a1 = considered_points[:len(considered_points)//2]
    candidates_a2 = considered_points[len(considered_points)//2:]

    # wyznaczenie punktów niezależnych
    a1 = help_divide(candidates_a1)
    a2 = help_divide(candidates_a2)

    # odjecie punktow ze zboru a1 i a2 ze zbioru considered, tak aby otrzymać u
    considered_points = list(set(considered_points) - set(a1)) + list(set(a1) - set(considered_points))
    considered_points = list(set(considered_points) - set(a2)) + list(set(a2) - set(considered_points))
    
    # posortowanie punktow od nowa, po konwersji ze zbioru
    considered_points = sorting_points(considered_points)

    # u = considered_points

    return a1, a2, considered_points

def field_of_square(A1: List[Tuple[int]], A2: List[Tuple[int]], U: List[Tuple[int]]) -> Dict[Tuple[int], List[object]]:

    '''
    funkcja licząca pola dla wyznaczonych kwadratów w zależności od danego U
    '''

    def help_square(A1: List[Tuple[int]], A2: List[Tuple[int]], u: Tuple[int]) -> List[object]:

        '''
        Funkcja pomocnicza, liczy pola dla konkretnego, jednego u
        '''

        areas = []
        for a1 in A1:
            for a2 in A2:
                if u[0] > max(a1[0], a2[0]): continue
                if u[1] > max(a1[1], a2[1]): continue
                area = abs(a2[1] - a1[1]) * abs(a2[0] - a1[0])
                areas.append(Areas(a1, a2, area))
        return areas

    areas = {u:help_square(A1, A2, u) for u in U }
    return areas  

def standardization_of_squares(areas: Dict[Tuple[int], List[object]]) -> Dict[Tuple[int], List[object]]:

    '''
    Funkcja standaryzująca pola kwadratow
    '''

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
    '''
    Posortowanie słownika klucz: u, wartość: lista punktów 
    tworząca pola wokół punktu u w zależności rosnącej względem pola kwadratu (area)
    '''

    for keys, values in areas.items():
        values.sort(key=lambda x:x.area)
    return areas

def main():

    points = [(0, 2), (1, 2), (1, 5), (2, 3), (2, 9), (3, 1), (3, 6), (3, 8), (4, 3), (4, 5), (4, 9), (5, 7), (6, 9), (6, 10), (7, 3), (7, 5), (7, 10), (8, 8), (9, 2), (9, 5), (9, 7), (9, 9), (10, 4), (10, 8), (10, 9), (11, 6), (11, 10), (12, 1), (12, 4), (12, 7)]
    limit = (len(points)//4) + 1
    sorting_points(points)
    A1, A2, U = divide_into_groups(points, limit)
    areas = field_of_square(A1, A2, U)
    areas = standardization_of_squares(areas)
    areas = ranking_creating(areas)
    a = 1

if __name__ == "__main__":

    main()

