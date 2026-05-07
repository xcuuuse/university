import random


def compute_g_l(word: list[int], argument: list[int]) -> tuple[int, int]:
    n = len(word)
    g = 0
    l = 0

    for i in range(n):
        a = argument[i]
        s = word[i]
        a_ = 1 - a
        s_ = 1 - s
        g_new = g | (a_ & s & (1 - l))
        l_new = l | (a & s_ & (1 - g))

        g, l = g_new, l_new

    return g, l


def generate_array(m: int, n: int, seed: int = 42) -> list[list[int]]:
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

def bool_xor(s: list[int], a: list[int], mask: list[int]) -> int:

    for i in range(len(s)):
        if mask[i] == 1 and (s[i] ^ a[i]) == 1:
            return 1
    return 0


def bool_equiv(s: list[int], a: list[int], mask: list[int]) -> int:
    for i in range(len(s)):
        if mask[i] == 1 and s[i] != a[i]:
            return 0
    return 1


def bool_or(s: list[int], a: list[int], mask: list[int]) -> int:
    for i in range(len(s)):
        if mask[i] == 1 and (s[i] | a[i]) == 1:
            return 1
    return 0


def bool_and(s: list[int], a: list[int], mask: list[int]) -> int:
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
def search_by_boolean(
    memory: list[list[int]],
    argument: list[int],
    mask: list[int],
    func_name: str,
    target_value: int = 1
) -> list[int]:
    func = BOOL_FUNCTIONS[func_name]
    result_flags = []

    for j, word in enumerate(memory):
        val = func(word, argument, mask)
        if val == target_value:
            result_flags.append(j)

    return result_flags


def count_matching_bits(s: list[int], a: list[int], mask: list[int]) -> int:
    return sum(1 for i in range(len(s)) if mask[i] == 1 and s[i] == a[i])


def search_max_match(memory, argument, mask):
    scores = [
        (j, count_matching_bits(word, argument, mask))
        for j, word in enumerate(memory)
    ]
    max_score = max(s for _, s in scores)
    return [j for j, s in scores if s == max_score], max_score

def print_separator(char='-', width=70):
    print(char * width)


def print_array(memory, title="Ассоциативный массив"):
    print(f"\n{'-'*70}")
    print(f"  {title}")
    print(f"{'-'*70}")
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


def main():
    M = 12
    N = 8
    memory = generate_array(M, N, seed=2025)
    print_array(memory, f"Ассоциативный массив ({M} слов * {N} бит)")
    print("\n" + "-"*70)
    print("  ПРОВЕРКА РЕКУРРЕНТНОГО АЛГОРИТМА (gji / lji)")
    print("-"*70)
    arg_demo = int_to_bits(130, N)
    print(f"\n  Аргумент A = {bits_str(arg_demo)} ({bits_to_int(arg_demo)})\n")
    print(f"  {'№':>4}  {'Слово':^{N+2}}  {'Dec':>5}  {'g':>3}  {'l':>3}  {'Результат'}")
    print_separator()
    for j, word in enumerate(memory):
        g, l = compute_g_l(word, arg_demo)
        if g == 0 and l == 0: rel = "S == A"
        elif g == 1 and l == 0: rel = "S >  A"
        else:                   rel = "S <  A"
        print(f"  [{j:>2}]  {bits_str(word)}  {bits_to_int(word):>5}  {g:>3}  {l:>3}  {rel}")
    print_separator()
    print("\n" + "-"*70)
    print("  ПОИСК 1: Логическая эквивалентность (EQUIV)")
    print("  Найти слова, у которых маскированные разряды совпадают с аргументом")
    print("-"*70)
    arg1  = int_to_bits(0b10110100, N)   # = 180
    mask1 = int_to_bits(0b11110000, N)   # маска: старшие 4 бита
    idx1  = search_by_boolean(memory, arg1, mask1, 'EQUIV', target_value=1)
    print_result(idx1, memory, arg1, mask1, 'EQUIV', 1)
    print("\n" + "-"*70)
    print("  ПОИСК 2: Исключающее ИЛИ (XOR)")
    print("  Найти слова, у которых ЕСТЬ расхождение с аргументом по маске")
    print("-"*70)
    arg2  = int_to_bits(0b01010101, N)   # = 85
    mask2 = int_to_bits(0b00111100, N)   # маска: биты 2..5
    idx2  = search_by_boolean(memory, arg2, mask2, 'XOR', target_value=1)
    print_result(idx2, memory, arg2, mask2, 'XOR', 1)
    print("\n" + "-"*70)
    print("  ПОИСК 3: Логическое И (AND)")
    print("  Найти слова, у которых ВСЕ маскированные биты совпадают с '1' аргумента")
    print("-"*70)
    arg3 = int_to_bits(0b11111111, N)   # все 1
    mask3 = int_to_bits(0b00001111, N)   # маска: младшие 4 бита
    idx3 = search_by_boolean(memory, arg3, mask3, 'AND', target_value=1)
    print_result(idx3, memory, arg3, mask3, 'AND', 1)
    print("\n" + "-"*70)
    print("  ПОИСК 4: Логическое ИЛИ (OR)")
    print("  Найти слова, у которых хоть один маскированный бит совпадает с '1' аргумента")
    print("-"*70)
    arg4  = int_to_bits(0b00000011, N)   # = 3
    mask4 = int_to_bits(0b11000011, N)   # крайние биты
    idx4  = search_by_boolean(memory, arg4, mask4, 'OR', target_value=1)
    print_result(idx4, memory, arg4, mask4, 'OR', 1)
    print("\n  Выполнение программы завершено.\n")


if __name__ == "__main__":
    main()