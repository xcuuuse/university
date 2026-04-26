"""
Лабораторная работа №7 — Вариант 5
Моделирование ассоциативного процессора: Поиск на основе булевых функций
"""

import random

# ─────────────────────────────────────────────
#  1. ВЫЧИСЛЕНИЕ ЛОГИЧЕСКИХ ПЕРЕМЕННЫХ gji / lji
# ─────────────────────────────────────────────

def compute_g_l(word: list[int], argument: list[int]) -> tuple[int, int]:
    """
    Рекуррентный алгоритм сравнения (формула 1, сравнение со старшего разряда).
    word, argument — списки бит (индекс 0 = старший разряд).
    Возвращает (g, l):
        g=0, l=0  →  word == argument
        g=1, l=0  →  word >  argument
        g=0, l=1  →  word <  argument
    """
    n = len(word)
    g = 0   # gj, n+1 = 0
    l = 0   # lj, n+1 = 0

    for i in range(n):        # от старшего (i=0) к младшему
        a  = argument[i]
        s  = word[i]
        a_ = 1 - a   # инверсия a
        s_ = 1 - s   # инверсия s

        # gji = gj,i+1 OR (NOT(ai) AND sji AND NOT(lj,i+1))
        g_new = g | (a_ & s & (1 - l))
        # lji = lj,i+1 OR (ai AND NOT(sji) AND NOT(gj,i+1))
        l_new = l | (a  & s_ & (1 - g))

        g, l = g_new, l_new

    return g, l


# ─────────────────────────────────────────────
#  2. ГЕНЕРАЦИЯ АССОЦИАТИВНОГО МАССИВА
# ─────────────────────────────────────────────

def generate_array(m: int, n: int, seed: int = 42) -> list[list[int]]:
    """Создаёт массив m слов по n бит (псевдослучайные числа)."""
    random.seed(seed)
    return [
        [random.randint(0, 1) for _ in range(n)]
        for _ in range(m)
    ]


def bits_to_int(bits: list[int]) -> int:
    result = 0
    for b in bits:
        result = (result << 1) | b
    return result


def int_to_bits(value: int, n: int) -> list[int]:
    return [(value >> (n - 1 - i)) & 1 for i in range(n)]


def bits_str(bits: list[int]) -> str:
    return ''.join(map(str, bits))


# ─────────────────────────────────────────────
#  3. БУЛЕВЫ ФУНКЦИИ ДЛЯ ПОИСКА
# ─────────────────────────────────────────────

def bool_xor(s: list[int], a: list[int], mask: list[int]) -> int:
    """
    XOR по маскированным разрядам.
    Возвращает значение булевой функции XOR между словом s и аргументом a
    (только по разрядам, где mask[i] == 1).
    Результат = OR всех (s[i] XOR a[i]) по маскированным позициям.
    Если хоть один разряд отличается → 1 (есть несовпадение).
    """
    for i in range(len(s)):
        if mask[i] == 1 and (s[i] ^ a[i]) == 1:
            return 1
    return 0


def bool_equiv(s: list[int], a: list[int], mask: list[int]) -> int:
    """
    Логическая эквивалентность по маскированным разрядам.
    Возвращает 1 если все маскированные разряды совпадают, иначе 0.
    """
    for i in range(len(s)):
        if mask[i] == 1 and s[i] != a[i]:
            return 0
    return 1


def bool_or(s: list[int], a: list[int], mask: list[int]) -> int:
    """
    ИЛИ по маскированным разрядам (s[i] OR a[i] для маск. позиций).
    Возвращает 1 если хоть один (s[i] OR a[i]) == 1.
    """
    for i in range(len(s)):
        if mask[i] == 1 and (s[i] | a[i]) == 1:
            return 1
    return 0


def bool_and(s: list[int], a: list[int], mask: list[int]) -> int:
    """
    И по маскированным разрядам (s[i] AND a[i] для маск. позиций).
    Возвращает 1 если ВСЕ (s[i] AND a[i]) == 1.
    """
    for i in range(len(s)):
        if mask[i] == 1 and (s[i] & a[i]) == 0:
            return 0
    return 1


BOOL_FUNCTIONS = {
    'XOR':   bool_xor,
    'EQUIV': bool_equiv,
    'OR':    bool_or,
    'AND':   bool_and,
}


# ─────────────────────────────────────────────
#  4. ПОИСКОВЫЕ ОПЕРАЦИИ НА ОСНОВЕ БУЛЕВЫХ ФУНКЦИЙ
# ─────────────────────────────────────────────

def search_by_boolean(
    memory: list[list[int]],
    argument: list[int],
    mask: list[int],
    func_name: str,
    target_value: int = 1
) -> list[int]:
    """
    Поиск слов, для которых булева функция func_name принимает значение target_value.

    memory       — ассоциативный массив (список слов)
    argument     — аргумент поиска (список бит)
    mask         — маска (1 = разряд участвует в поиске)
    func_name    — 'XOR', 'EQUIV', 'OR', 'AND'
    target_value — искомое значение функции (0 или 1)

    Возвращает список индексов слов-результатов.
    """
    func = BOOL_FUNCTIONS[func_name]
    result_flags = []

    for j, word in enumerate(memory):
        val = func(word, argument, mask)
        if val == target_value:
            result_flags.append(j)

    return result_flags


def count_matching_bits(s: list[int], a: list[int], mask: list[int]) -> int:
    """Подсчёт совпадающих битов по маске (для поиска по соответствию XOR)."""
    return sum(1 for i in range(len(s)) if mask[i] == 1 and s[i] == a[i])


def search_max_match(memory, argument, mask):
    """Находит слова с максимальным числом совпадений по маске."""
    scores = [
        (j, count_matching_bits(word, argument, mask))
        for j, word in enumerate(memory)
    ]
    max_score = max(s for _, s in scores)
    return [j for j, s in scores if s == max_score], max_score


# ─────────────────────────────────────────────
#  5. ВЫВОД / ДЕМОНСТРАЦИЯ
# ─────────────────────────────────────────────

def print_separator(char='─', width=70):
    print(char * width)


def print_array(memory, title="Ассоциативный массив"):
    print(f"\n{'═'*70}")
    print(f"  {title}")
    print(f"{'═'*70}")
    print(f"  {'№':>4}  {'Биты':^{len(memory[0])+2}}  {'Десятичное':>10}")
    print_separator()
    for j, word in enumerate(memory):
        print(f"  [{j:>2}]  {bits_str(word)}  {bits_to_int(word):>10}")
    print_separator()


def print_result(indices, memory, argument, mask, func_name, target):
    n = len(memory[0])
    print(f"\n  Аргумент поиска : {bits_str(argument)}  ({bits_to_int(argument)})")
    print(f"  Маска           : {bits_str(mask)}")
    print(f"  Булева функция  : {func_name}  ==  {target}")
    print_separator()
    if not indices:
        print("  Результат: слов не найдено.")
    else:
        print(f"  Найдено слов: {len(indices)}")
        print_separator()
        for j in indices:
            word = memory[j]
            print(f"  [{j:>2}]  {bits_str(word)}  ({bits_to_int(word):>5})")
    print_separator()


# ─────────────────────────────────────────────
#  6. ГЛАВНАЯ ФУНКЦИЯ — ДЕМОНСТРАЦИЯ
# ─────────────────────────────────────────────

def main():
    M = 12   # количество слов
    N = 8    # разрядность

    print("\n" + "═"*70)
    print("  ЛАБОРАТОРНАЯ РАБОТА №7  |  ВАРИАНТ 5")
    print("  Ассоциативный процессор: поиск на основе булевых функций")
    print("═"*70)

    # Генерация массива
    memory = generate_array(M, N, seed=2025)
    print_array(memory, f"Ассоциативный массив ({M} слов × {N} бит)")

    # Демонстрация рекуррентного алгоритма gji / lji
    print("\n" + "═"*70)
    print("  ПРОВЕРКА РЕКУРРЕНТНОГО АЛГОРИТМА (gji / lji)")
    print("═"*70)
    arg_demo = int_to_bits(130, N)
    print(f"\n  Аргумент A = {bits_str(arg_demo)} ({bits_to_int(arg_demo)})\n")
    print(f"  {'№':>4}  {'Слово':^{N+2}}  {'Dec':>5}  {'g':>3}  {'l':>3}  {'Результат'}")
    print_separator()
    for j, word in enumerate(memory):
        g, l = compute_g_l(word, arg_demo)
        if   g == 0 and l == 0: rel = "S == A"
        elif g == 1 and l == 0: rel = "S >  A"
        else:                   rel = "S <  A"
        print(f"  [{j:>2}]  {bits_str(word)}  {bits_to_int(word):>5}  {g:>3}  {l:>3}  {rel}")
    print_separator()

    # ── Поиск 1: EQUIV — маскированное равенство ──────────────────────────
    print("\n" + "═"*70)
    print("  ПОИСК 1: Логическая эквивалентность (EQUIV)")
    print("  Найти слова, у которых маскированные разряды совпадают с аргументом")
    print("═"*70)
    arg1  = int_to_bits(0b10110100, N)   # = 180
    mask1 = int_to_bits(0b11110000, N)   # маска: старшие 4 бита
    idx1  = search_by_boolean(memory, arg1, mask1, 'EQUIV', target_value=1)
    print_result(idx1, memory, arg1, mask1, 'EQUIV', 1)

    # ── Поиск 2: XOR — несовпадение хотя бы одного бита ──────────────────
    print("\n" + "═"*70)
    print("  ПОИСК 2: Исключающее ИЛИ (XOR)")
    print("  Найти слова, у которых ЕСТЬ расхождение с аргументом по маске")
    print("═"*70)
    arg2  = int_to_bits(0b01010101, N)   # = 85
    mask2 = int_to_bits(0b00111100, N)   # маска: биты 2..5
    idx2  = search_by_boolean(memory, arg2, mask2, 'XOR', target_value=1)
    print_result(idx2, memory, arg2, mask2, 'XOR', 1)

    # ── Поиск 3: AND — все маскированные биты равны 1 ─────────────────────
    print("\n" + "═"*70)
    print("  ПОИСК 3: Логическое И (AND)")
    print("  Найти слова, у которых ВСЕ маскированные биты совпадают с '1' аргумента")
    print("═"*70)
    arg3  = int_to_bits(0b11111111, N)   # все 1
    mask3 = int_to_bits(0b00001111, N)   # маска: младшие 4 бита
    idx3  = search_by_boolean(memory, arg3, mask3, 'AND', target_value=1)
    print_result(idx3, memory, arg3, mask3, 'AND', 1)

    # ── Поиск 4: OR — хотя бы один бит из маски ненулевой ────────────────
    print("\n" + "═"*70)
    print("  ПОИСК 4: Логическое ИЛИ (OR)")
    print("  Найти слова, у которых хоть один маскированный бит совпадает с '1' аргумента")
    print("═"*70)
    arg4  = int_to_bits(0b00000011, N)   # = 3
    mask4 = int_to_bits(0b11000011, N)   # крайние биты
    idx4  = search_by_boolean(memory, arg4, mask4, 'OR', target_value=1)
    print_result(idx4, memory, arg4, mask4, 'OR', 1)

    # ── Поиск 5: максимальное совпадение (расширение) ─────────────────────
    print("\n" + "═"*70)
    print("  ПОИСК 5: Максимальное совпадение (Best Match)")
    print("  Найти слово(а) с наибольшим числом совпадающих бит по маске")
    print("═"*70)
    arg5  = int_to_bits(0b10101010, N)
    mask5 = int_to_bits(0b11111111, N)   # все разряды
    best_idx, best_score = search_max_match(memory, arg5, mask5)
    print(f"\n  Аргумент  : {bits_str(arg5)}  ({bits_to_int(arg5)})")
    print(f"  Маска     : {bits_str(mask5)}")
    print(f"  Максимум совпадений: {best_score} из {N}")
    print_separator()
    for j in best_idx:
        word = memory[j]
        print(f"  [{j:>2}]  {bits_str(word)}  ({bits_to_int(word):>5})")
    print_separator()

    print("\n  Выполнение программы завершено.\n")


if __name__ == "__main__":
    main()