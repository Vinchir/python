import numpy as np
import json
import re


def section_length(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 +
            (point1[2] - point2[2]) ** 2) ** (1 / 2)


def vector_length(vec):
    return (vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2) ** (1 / 2)


with open('data.txt') as data:
    dict_obj = data.read()
dict_obj = re.sub(r'([a-z]+)', r'"\1"', dict_obj)
dict_obj = re.sub(r'(\[[0-9|, .-]*])..(\[[0-9|, .-]*])',
                  r'"cord1": \1, "cord2": \2', dict_obj)
dict_obj = json.loads(dict_obj)
cord1 = np.array(tuple(dict_obj['line']['cord1']))
cord2 = np.array(tuple(dict_obj['line']['cord2']))
center = np.array(tuple(dict_obj['sphere']['center']))
radius = float(dict_obj['sphere']['radius'])

# нормаль к плоскости
V = np.cross(cord2 - center, cord1 - center)
# длина отрезка
AB = section_length(cord2, cord1)
# расстояние от центра до прямой
h = vector_length(V) / AB
# перпендикуляр из центра на прямую
OP = np.cross(V, cord2-cord1)
OP = OP / vector_length(OP)
# основание перпендикуляра из центра на прямую
P = center + OP * h
# Расстояние d от точки P до точек пересечения сферы и прямой
d = abs(radius ** 2 - h ** 2) ** (1 / 2)
# Вектор Pd на прямой AB
Pd = (cord2 - cord1) / AB * d
# точки пересечения
P1 = Pd + P
P2 = P - Pd

if vector_length(P1 - center) == radius and vector_length(P2 - center) == radius:
    print(P1, '\n', P2)
else:
    print('Коллизий не найдено')
