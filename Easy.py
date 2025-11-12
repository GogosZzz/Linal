from itertools import product
from typing import List, Tuple, Dict
import math
import time
from sympy import factorint


def is_prime(num: int) -> bool:
    if num <= 1:
        return False
    if num == 2:
        return True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def sieve(n: int) -> List[bool]:
    sieve_list_in_def = [True] * (n + 1)
    sieve_list_in_def[0] = sieve_list_in_def[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve_list_in_def[i]:
            for j in range(i * i, n + 1, i):
                sieve_list_in_def[j] = False
    return sieve_list_in_def


def is_palindrome(num: int) -> bool:
    str_num = str(num)
    return str_num == str_num[::-1]


def get_rotations(num: int) -> List[int]:
    str_num = str(num)
    return [int(str_num[i:] + str_num[:i]) for i in range(len(str_num))]


def gcd_mine(a: int, b: int) -> int:
    """
    Вычисляет НОД двух чисел
    Использует алгоритм Евклида
    """
    # Обрабатываем отрицательные числа
    a, b = abs(a), abs(b)

    # Алгоритм Евклида
    while b != 0:
        a, b = b, a % b
    return a


def factorint_mine(num: int) -> Dict[int, int]:
    """
    Разлагает число на простые множители
    """
    if num <= 1:
        return {}

    factors = {}

    # Обрабатываем 2 отдельно
    count = 0
    while num % 2 == 0:
        count += 1
        num //= 2
    if count > 0:
        factors[2] = count

    # Обрабатываем нечётные числа
    divisor = 3
    while divisor * divisor <= num:
        if num % divisor == 0:
            count = 0
            while num % divisor == 0:
                count += 1
                num //= divisor
            factors[divisor] = count
        divisor += 2

    # Если остаток простой
    if num > 1:
        factors[num] = 1

    return factors


sieve_list = sieve(10 ** 6)



# =========Задача 1===========
def palindromic_squares_and_circular_primes() -> tuple[List[int], List[int]]:
    """
    Возвращает:
    tuple:
    - список всех палиндромов a < 100000, для которых a^2 — палиндром;
    - список всех простых p < 1000000, все циклические перестановки цифр которых
    ,→ просты.
    """
    # Подзадача 1
    palindrome_list = []
    for num in range(1, 10 ** 5):
        if is_palindrome(num):
            if is_palindrome(num ** 2):
                palindrome_list.append(num)

    # Подзадача 2
    circular_primes_list = []
    for num in range(1, 10 ** 6):
        if sieve_list[num]:
            rotations = get_rotations(num)
            if all(sieve_list[r] for r in rotations):
                circular_primes_list.append(num)

    return palindrome_list, circular_primes_list


# =========Задача 2===========
def palindromic_cubes_and_palindromic_primes() -> tuple[List[int], List[int]]:
    """
    Возвращает:
    tuple:
    - список всех палиндромов a < 100000, для которых a^3 — палиндром;
    - список всех простых p <= 10000, которые являются палиндромами.
    """
    palindrome_list = []
    prime_palindrome_list = []
    for num in range(1, 10 ** 5):
        if is_palindrome(num):
            if is_palindrome(num ** 3):
                palindrome_list.append(num)

    for num in range(1, 10001):
        if sieve_list[num] and is_palindrome(num):
            prime_palindrome_list.append(num)
    return palindrome_list, prime_palindrome_list


# =========Задача 3===========
def primes_with_two_digits() -> Dict[str, List[int]]:
    """
    Возвращает словарь вида:
    {
    '13': [список первых 100 простых из {1,3}],
    '15': [список первых 100 простых из {1,5}],
    '17': [список первых 100 простых из {1,7}],
    '19': [список первых 100 простых из {1,9}]
    }
    """
    result = {
        '13': [],
        '15': [],
        '17': [],
        '19': []
    }

    # Соответствие меток и цифр
    digit_pairs = {
        '13': ('1', '3'),
        '15': ('1', '5'),
        '17': ('1', '7'),
        '19': ('1', '9')
    }

    for key, (d1, d2) in digit_pairs.items():
        primes_list = []
        length = 1

        # Генерируем числа увеличивающейся длины, пока не наберем 100 простых
        while len(primes_list) < 100:
            for comb in product([d1, d2], repeat=length):
                num_str = ''.join(comb)
                num = int(num_str)

                # Проверяем на простоту и добавляем, если еще нет в списке
                if is_prime(num) and num not in primes_list:
                    primes_list.append(num)

                if len(primes_list) >= 100:
                    break

            length += 1

        # Сортируем по возрастанию и берем первые 100
        primes_list.sort()
        result[key] = primes_list[:100]

    return result


# =========Задача 4===========
def twin_primes_analysis(limit_pairs: int = 1000) -> Tuple[List[Tuple[int, int]], List[float]]:
    """
    Возвращает:
    - список первых `limit_pairs` пар близнецов (p, p+2);
    - список значений отношения pi_2(n) / pi(n) для n, соответствующих последним
    ,→ элементам каждой пары,
    где pi_2(n) — количество пар близнецов <= n, pi(n) — количество простых <= n.
    """
    twin_primes = []
    ratios = []

    prime_cnt = 2
    twin_cnt = 0

    for num in range(5, 10 ** 6, 2):
        if is_prime(num):
            prime_cnt += 1

            if is_prime(num - 2):
                twin_cnt += 1
                twin_primes.append((num - 2, num))
                ratio = twin_cnt / prime_cnt
                ratios.append(ratio)

                if len(twin_primes) >= limit_pairs:
                    break

    return twin_primes, ratios


# =========Задача 5===========
def factorial_plus_one_factors() -> Dict[int, Dict[int, int]]:
    """
    Возвращает словарь вида:
    { n: {простой_делитель: степень, ...}, ... }
    для n от 2 до 50, где ключ — n, значение — разложение n! + 1 на простые множители.
    """
    result = {}

    for n in range(2, 51):
        factorial = math.factorial(n) + 1
        factors = factorint(factorial)
        result[n] = factors

    return result


# =========Задача 6===========
def euler_phi_direct(n: int) -> int:
    """
    Вычисляет (n) прямым перебором.
    """
    cnt = 0
    for k in range(1, n + 1):
        if gcd_mine(n, k):
            cnt += 1
    return cnt


def euler_phi_factor(n: int) -> int:
    """
    Вычисляет (n) через разложение на простые множители.
    """
    result = n
    factors = factorint_mine(n)
    for p in factors:
        result *= (1 - 1 / p)
    return int(result)


def compare_euler_phi_methods(test_values: List[int]) -> dict:
    """
    Сравнивает время работы трёх методов на заданных значениях.
    Возвращает словарь с тремя списками времён (в секундах).
    """
    times_direct = []
    times_factor = []
    times_sympy = []

    for n in test_values:
        # Метод 1: прямой перебор
        start = time.time()
        euler_phi_direct(n)
        times_direct.append(time.time() - start)

        # Метод 2: через разложение
        start = time.time()
        euler_phi_factor(n)
        times_factor.append(time.time() - start)

        # Метод 3: sympy
        start = time.time()
        sympy.totient(n)
        times_sympy.append(time.time() - start)

    return {
        'direct': times_direct,
        'factor': times_factor,
        'sympy': times_sympy
    }


# 1
print('задача №1\n', palindromic_squares_and_circular_primes(), '\n')

# 2
print('задача №2\n', palindromic_cubes_and_palindromic_primes(), '\n')

# 3
print('задача №3')
primes_dict = primes_with_two_digits()
for key, primes in primes_dict.items():
    print(f"{key}: {primes[:]}")
# 4
print("\n=== Задача 4: Простые-близнецы ===")
twins, ratios = twin_primes_analysis(100)
print(f"Первые 5 пар близнецов: {twins[:]}")
print(f"Последние 5 отношений: {ratios[:]}")
