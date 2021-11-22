from typing import List, Tuple, Set, Dict
# totalnie do dokończenia, ale muszę iść spać xd
def sorting_points(points: List[Tuple[int]]) -> List[Tuple[int]]:

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

    def help_divide(points: List[Tuple[int]]) -> List[Tuple[int]]:
        considered = points[0]
        set_a = [points]

        # wyznaczamy punkty niezależne
        while len(set_a) == 1:
            set_a = [considered]
            for point in points[1:]:
                if (point[0] > considered[0]) ^ (point[1] > considered[1]):
                    set_a.append(point)
            points = points[1:]
            considered = points[0]

        set_better = [set_a[0]]

        # co jeśli jednak nie są niezależne?
        # sprawdzamy czy nie mają którejś współrzędnej tej samej
        for a_elem in set_a[1:]:
            choice = True
            for b_elem in set_better:
                if a_elem[0] == b_elem[0] or a_elem[1] == b_elem[1]:
                    choice = False
                if a_elem[0] == b_elem[1] or a_elem[1] == b_elem[0]:
                    choice = False
                # if a_elem == (2, 9):
                #     a = a_elem[0] > b_elem[0]
                #     b = a_elem[1] > b_elem[1]
                # if not((a_elem[0] > b_elem[1]) ^ (a_elem[1] < b_elem[0])):
                #     choice = False
            if choice:
                set_better.append(a_elem)

        return set_better

    # podział punktów na grupy: idealne, antyidealne i rozpatrywane
    # ideal_points = points[:limit]
    # nadir_points = points[-limit:]
    considered_points = points[limit:-limit]

    candidates_a1 = considered_points[:len(considered_points)//2]
    candidates_a2 = considered_points[len(considered_points)//2:]

    a1 = help_divide(candidates_a1)
    a2 = help_divide(candidates_a2)

    considered_points = list(set(considered_points) - set(a1)) + list(set(a1) - set(considered_points))
    considered_points = list(set(considered_points) - set(a2)) + list(set(a2) - set(considered_points))
    
    considered_points = sorting_points(considered_points)

    # u = considered_points

    return a1, a2, considered_points

def field_of_square(A1: List[Tuple[int]], A2: List[Tuple[int]], u: List[Tuple[int]]):

    def help_square(A1: List[Tuple[int]], A2: List[Tuple[int]], u: Tuple[int]):
        areas = []
        for a1 in A1:
            for a2 in A2:
                if u[0] > max(a1[0], a2[0]): continue
                if u[1] > max(a1[1], a2[1]): continue
                area = abs(a2[1] - a1[1]) * abs(a2[0] - a1[0])
                areas.append([(a1, a2), area])
        return areas

    areas = {u:help_square(A1, A2, u) for u in U }
    return areas  

def standardization_of_squares(areas):

    help_sum = {}
    for k, val in areas.items():
        temp = [v[1] for v in val]
        help_sum[k] = sum(temp)
    temp = []
    for keys, values in areas.items():
        for val in values:
            temp.append([val[0], val[1]/help_sum[keys]])
        areas[keys] = temp
    return areas

def ranking_creating(areas):
    # temp = []
    # for keys, values in areas.items():
    #     for val in values:
    #         temp.append([val[0], val[1]/help_sum[keys]])
    #     areas[keys] = temp
    # # return areas    
    # for i in range(len(points)-1):
    #     for j in range(len(points)-i-1):
    #         if points[j][0]**2 + points[j][1]**2 > points[j+1][0]**2 + points[j+1][1]**2:
    #             temp = points[j]
    #             points[j] = points[j+1]
    #             points[j+1] = temp
    return




points = [(0, 2), (1, 2), (1, 5), (2, 3), (2, 9), (3, 1), (3, 6), (3, 8), (4, 3), (4, 5), (4, 9), (5, 7), (6, 9), (6, 10), (7, 3), (7, 5), (7, 10), (8, 8), (9, 2), (9, 5), (9, 7), (9, 9), (10, 4), (10, 8), (10, 9), (11, 6), (11, 10), (12, 1), (12, 4), (12, 7)]
limit = (len(points)//4) + 1
sorting_points(points)
A1, A2, U = divide_into_groups(points, limit)
areas = field_of_square(A1, A2, U)
areas = standardization_of_squares(areas)
print(areas)
areas = ranking_creating(areas)


a=1
