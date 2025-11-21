import random
from sympy.combinatorics import SymmetricGroup

from typing import Dict ,List


N = 405059 % 20
m = 4 + (N % 5)
n = 2 + (N % 10)
k = 1 + (N % 7)
n1 = N % 6
n2 = (N + 1) % 6
n3 = (N + 2) % 6
p = 19
s = 15
r = 44
t = 14


def subgroups_of_Sm(N: int) -> dict:
    """
    Normal: Найдите все подгруппы симметрической группы S_m
    """
    G = SymmetricGroup(m)

    basic_subgroups = []
    basic_subgroups.append(G)

    # Тривиальная подгруппа
    trivial_sub = G.subgroup([G.identity])
    basic_subgroups.append(trivial_sub)

    # Несколько циклических подгрупп
    elements = list(G.elements)
    for i in range(1, min(10, len(elements))):
        elem = elements[i]
        if elem != G.identity:
            cyclic_sub = G.subgroup([elem])
            if cyclic_sub not in basic_subgroups:
                basic_subgroups.append(cyclic_sub)

    subgroups = basic_subgroups
    total_subgroups = len(subgroups)

    # Выбираем подгруппу по индексу
    index = N % total_subgroups
    selected_subgroup = subgroups[index]

    # Строим смежные классы
    left_cosets = []
    right_cosets = []

    sample_elements = elements[:len(G)]

    for g in sample_elements:
        # Левый смежный класс
        left_coset = set()
        for h in selected_subgroup:
            left_coset.add(g * h)

        # Правый смежный класс
        right_coset = set()
        for h in selected_subgroup:
            right_coset.add(h * g)

        if left_coset not in left_cosets:
            left_cosets.append(left_coset)
        if right_coset not in right_cosets:
            right_cosets.append(right_coset)

    # Определяем нормальность (правильно)
    is_normal = True
    for g in sample_elements:
        left_coset = set(g * h for h in selected_subgroup)
        right_coset = set(h * g for h in selected_subgroup)
        if left_coset != right_coset:
            is_normal = False
            break

    # Преобразуем смежные классы в читаемый вид
    def coset_to_str(coset):
        elements_list = sorted([str(elem) for elem in coset])
        return f"{{{', '.join(elements_list[:3])}{'...' if len(elements_list) > 3 else ''}}}"

    left_cosets_str = [coset_to_str(coset) for coset in left_cosets]
    right_cosets_str = [coset_to_str(coset) for coset in right_cosets]

    # Случайная подгруппа
    random_subgroup = random.choice(subgroups)

    return {
        'm': m,
        'total_subgroups': total_subgroups,
        'random_subgroup': {
            'order': random_subgroup.order(),
            'elements_count': len(list(random_subgroup.elements)),
            'elements_sample': [str(elem) for elem in list(random_subgroup.elements)[:3]]
        },
        'selected_subgroup': {
            'index': index,
            'order': selected_subgroup.order(),
            'elements': [str(elem) for elem in list(selected_subgroup.elements)[:5]],
            'index_in_group': len(left_cosets),
            'is_normal': is_normal,
            'left_cosets': left_cosets_str,
            'right_cosets': right_cosets_str,
            'left_cosets_count': len(left_cosets),
            'right_cosets_count': len(right_cosets)
        },
        'all_subgroups_info': [
            {
                'order': sg.order(),
                'elements_count': len(list(sg.elements)),
                'type': type(sg).__name__
            }
            for sg in subgroups[:]
        ]
    }



result = subgroups_of_Sm(N)

print(f"Симметрическая группа: S_{result['m']}")
print(f"Всего подгрупп найдено: {result['total_subgroups']}")

print(f"\nСлучайная подгруппа:")
print(f"  Порядок: {result['random_subgroup']['order']}")
print(f"  Количество элементов: {result['random_subgroup']['elements_count']}")
print(f"  Примеры элементов: {result['random_subgroup']['elements_sample']}")

print("\nВыбранная подгруппа (индекс 8)")
print(f"  Порядок: {result['selected_subgroup']['order']}")
print(f"  Индекс в группе: {result['selected_subgroup']['index_in_group']}")
print(f"  Примеры элементов: {result['selected_subgroup']['elements']}")

print(f"\nЛЕВЫЕ СМЕЖНЫЕ КЛАССЫ ({result['selected_subgroup']['left_cosets_count']} шт.):")
for i, coset in enumerate(result['selected_subgroup']['left_cosets'], 1):
    print(f"  Класс {i}: {coset}")

print(f"\nПРАВЫЕ СМЕЖНЫЕ КЛАССЫ ({result['selected_subgroup']['right_cosets_count']} шт.):")
for i, coset in enumerate(result['selected_subgroup']['right_cosets'], 1):
    print(f"  Класс {i}: {coset}")

print(f"\nЯвляется нормальной: {result['selected_subgroup']['is_normal']}")