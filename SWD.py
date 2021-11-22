from typing import List, Tuple, Set, Dict
#totalnie do dokończenia, ale muszę iść spać xd
# def sorting_points(points: List[Tuple[int]]) -> List[Tuple[int]]:
#
#     # ułożenie punktów w liście w zależności od odpegłości od punktu (0,0)
#     # sortowanie bąbelkowe
#     for i in range(len(points)-1):
#         for j in range(len(points)-i-1):
#             if points[j][0]**2 + points[j][1]**2 > points[j+1][0]**2 + points[j+1][1]**2:
#                 temp = points[j]
#                 points[j] = points[j+1]
#                 points[j+1] = temp
#     # print(points)
#     return points

def sorting_points(points: List[Tuple[int]]) -> List[Tuple[int]]:
    abc = sorted(points,key = lambda x: (x[0]**2 + x[1]**2)**0.5)
    # print(abc)
    return abc

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
points = sorting_points(points)
A1, A2, U = divide_into_groups(points, limit)
areas = field_of_square(A1, A2, U)
areas = standardization_of_squares(areas)
areas = ranking_creating(areas)


a=1
