from itertools import product


def build_truth_table():
    table = []
    for x1, x2, x3 in product([0, 1], repeat=3):
        total = x1 + x2 + x3
        s = total % 2
        c = total // 2
        table.append((x1, x2, x3, s, c))
    return table


def print_truth_table(table):
    print("\n" + "=" * 50)
    print("  ТАБЛИЦА ИСТИННОСТИ ОДС-3")
    print("=" * 50)
    print(f"  № | X1  X2  X3 | Si  Ci+1")
    print("-" * 34)
    for idx, (x1, x2, x3, s, c) in enumerate(table):
        print(f"  {idx} |  {x1}   {x2}   {x3} |  {s}    {c}")
    print("=" * 50)


def get_minterms(table, func_index):
    return [row[:3] for row in table if row[func_index] == 1]


def minterm_to_str(minterm, var_names):
    parts = []
    for val, name in zip(minterm, var_names):
        parts.append(name if val == 1 else f"!{name}")
    return "(" + " * ".join(parts) + ")"


def build_sdnf(minterms, var_names):
    if not minterms:
        return "0"
    constituents = [minterm_to_str(m, var_names) for m in minterms]
    return " + ".join(constituents)


def print_sdnf(table, var_names=("X1", "X2", "X3")):
    print("\n" + "=" * 50)
    print("  СДНФ ВЫХОДНЫХ ФУНКЦИЙ")
    print("=" * 50)

    for func_idx, func_name in [(3, "Si"), (4, "Ci+1")]:
        minterms = get_minterms(table, func_idx)
        sdnf_str = build_sdnf(minterms, var_names)
        nums = [i for i, row in enumerate(table) if row[func_idx] == 1]
        print(f"\n  {func_name} СДНФ = +m{nums}")
        print(f"  {func_name} = {sdnf_str}")


def minterms_to_indices(minterms):
    return [int("".join(map(str, m)), 2) for m in minterms]


def can_merge(a, b):
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    return len(diff) == 1


def merge(a, b):
    return tuple(a[i] if a[i] == b[i] else None for i in range(len(a)))


def quine_mccluskey(minterms):
    if not minterms:
        return []

    groups = {}
    for m in minterms:
        ones = sum(b for b in m if b is not None)
        groups.setdefault(ones, []).append(m)

    prime_implicants = []
    used = set()

    while True:
        new_groups = {}
        merged_any = False
        keys = sorted(groups.keys())

        for i in range(len(keys) - 1):
            g1 = groups[keys[i]]
            g2 = groups[keys[i + 1]]
            for a in g1:
                for b in g2:
                    if can_merge(a, b):
                        merged = merge(a, b)
                        ones = sum(bit for bit in merged if bit is not None)
                        new_groups.setdefault(ones, [])
                        if merged not in new_groups[ones]:
                            new_groups[ones].append(merged)
                        used.add(a)
                        used.add(b)
                        merged_any = True

        for key, group in groups.items():
            for m in group:
                if m not in used:
                    if m not in prime_implicants:
                        prime_implicants.append(m)

        if not merged_any:
            break

        groups = new_groups
        used = set()

    unique = []
    for p in prime_implicants:
        if p not in unique:
            unique.append(p)
    return unique


def implicant_to_str(impl, var_names):
    parts = []
    for val, name in zip(impl, var_names):
        if val is None:
            continue
        parts.append(name if val == 1 else f"!{name}")
    if not parts:
        return "1"
    return " * ".join(parts)


def essential_cover(prime_implicants, minterms):
    def covers(pi, minterm):
        return all(pi[i] is None or pi[i] == minterm[i] for i in range(len(minterm)))

    coverage = {m: [pi for pi in prime_implicants if covers(pi, m)] for m in minterms}

    selected = []
    uncovered = set(minterms)
    for m, pis in coverage.items():
        if len(pis) == 1 and pis[0] not in selected:
            selected.append(pis[0])
    for pi in selected:
        uncovered = {m for m in uncovered if not covers(pi, m)}

    while uncovered:
        best = max(prime_implicants,
                   key=lambda pi: sum(1 for m in uncovered if covers(pi, m)))
        selected.append(best)
        prime_implicants = [p for p in prime_implicants if p != best]
        uncovered = {m for m in uncovered if not covers(best, m)}

    return selected


def minimize_function(minterms, var_names, func_name):
    if not minterms:
        return func_name + " = 0"

    prime_implicants = quine_mccluskey(minterms)
    essential = essential_cover(prime_implicants, minterms)
    terms = [implicant_to_str(pi, var_names) for pi in essential]
    return func_name + " = " + " + ".join(terms)


def print_minimization(table, var_names=("X1", "X2", "X3")):
    print("\n" + "=" * 50)
    print("  МИНИМИЗАЦИЯ (метод Квайна–МакКласки)")
    print("=" * 50)

    results = {}
    for func_idx, func_name in [(3, "Si"), (4, "Ci+1")]:
        minterms = get_minterms(table, func_idx)
        result = minimize_function(minterms, var_names, func_name)
        results[func_name] = result
        print(f"\n  {result}")

    print()
    return results


def multi_output_synthesis(table, var_names=("X1", "X2", "X3")):
    print("\n" + "=" * 50)
    print("  СИНТЕЗ КАК УСТРОЙСТВА С НЕСКОЛЬКИМИ ВЫХОДАМИ")
    print("=" * 50)

    mt_s = set(get_minterms(table, 3))
    mt_c = set(get_minterms(table, 4))
    common = mt_s & mt_c

    def fmt_set(s):
        return "{" + ", ".join(str(minterm_to_str(m, var_names)) for m in sorted(s)) + "}"

    print(f"\n  Минтермы Si   : {fmt_set(mt_s)}")
    print(f"  Минтермы Ci+1 : {fmt_set(mt_c)}")
    print(f"  Общие минтермы: {fmt_set(common)}")
    print(f"\n  Количество общих минтермов: {len(common)}")

    if common:
        print("\n  Общие конституэнты могут быть реализованы")
        print("  одними логическими элементами для обоих выходов.")
        common_str = " + ".join(minterm_to_str(m, var_names) for m in sorted(common))
        print(f"\n  Общая часть: {common_str}")

        only_s = mt_s - common
        only_c = mt_c - common
        if only_s:
            only_s_str = " + ".join(minterm_to_str(m, var_names) for m in sorted(only_s))
            print(f"\n  Только для Si  : {only_s_str}")
        if only_c:
            only_c_str = " + ".join(minterm_to_str(m, var_names) for m in sorted(only_c))
            print(f"  Только для Ci+1: {only_c_str}")

    print()


def print_circuit_description(table):

    print("\n" + "=" * 50)
    print("  ОПИСАНИЕ ЛОГИЧЕСКОЙ СХЕМЫ ОДС-3")
    print("=" * 50)

    print("""
  Входы: X1, X2, X3
  Выходы: Si (сумма), Ci+1 (перенос)

  ┌──────────────────────────────────────────┐
  │  Инверторы (НЕ):                         │
  │    !X1,  !X2,  !X3                       │
  ├──────────────────────────────────────────┤
  │  Конституэнты Si (схемы И на 3 входа):   │
  │    m1 = !X1 * !X2 *  X3                 │
  │    m2 = !X1 *  X2 * !X3                 │
  │    m4 =  X1 * !X2 * !X3                 │
  │    m7 =  X1 *  X2 *  X3                 │
  ├──────────────────────────────────────────┤
  │  Конституэнты Ci+1 (схемы И на 3 входа): │
  │    m3 = !X1 *  X2 *  X3                 │
  │    m5 =  X1 * !X2 *  X3                 │
  │    m6 =  X1 *  X2 * !X3                 │
  │    m7 =  X1 *  X2 *  X3  (общая!)       │
  ├──────────────────────────────────────────┤
  │  Сумматоры выходов (схемы ИЛИ):          │
  │    Si   = m1 + m2 + m4 + m7             │
  │    Ci+1 = m3 + m5 + m6 + m7             │
  ├──────────────────────────────────────────┤
  │  Оценка оборудования:                    │
  │    3  элемента НЕ                        │
  │    7  элементов И  (3 входа)  — *        │
  │    2  элемента ИЛИ (4 входа)             │
  │    * m7 общий: реально 7 вентилей И      │
  └──────────────────────────────────────────┘

  Схема ОДС-3 (текстовое представление):

  X1 ──┬──[НЕ]──!X1──┐
       │              ├─[И]── m1(!X1·!X2·X3)  ─┐
  X2 ──┼──[НЕ]──!X2──┤                          │
       │              ├─[И]── m2(!X1·X2·!X3)  ──┤
  X3 ──┴──[НЕ]──!X3──┘                          │
                      ├─[И]── m4(X1·!X2·!X3)  ──┼──[ИЛИ]── Si
                      │                          │
                      ├─[И]── m7(X1·X2·X3)    ──┤
                      │                          │
                      ├─[И]── m3(!X1·X2·X3)   ──┤
                      │                          │
                      ├─[И]── m5(X1·!X2·X3)   ──┼──[ИЛИ]── Ci+1
                      │                          │
                      └─[И]── m6(X1·X2·!X3)   ──┘
""")


def verify(table):

    print("=" * 50)
    print("  ВЕРИФИКАЦИЯ СХЕМЫ")
    print("=" * 50)
    errors = 0
    for x1, x2, x3, s_exp, c_exp in table:
        s_calc = (
                (not x1 and not x2 and x3) or
                (not x1 and x2 and not x3) or
                (x1 and not x2 and not x3) or
                (x1 and x2 and x3)
        )

        c_calc = (
                (not x1 and x2 and x3) or
                (x1 and not x2 and x3) or
                (x1 and x2 and not x3) or
                (x1 and x2 and x3)
        )
        s_calc = int(s_calc)
        c_calc = int(c_calc)
        status = "OK" if s_calc == s_exp and c_calc == c_exp else "ОШИБКА"
        if status == "ОШИБКА":
            errors += 1
        print(f"  X1={x1} X2={x2} X3={x3} | Si={s_calc}(ожид={s_exp}) "
              f"Ci+1={c_calc}(ожид={c_exp})  [{status}]")

    print()
    if errors == 0:
        print("  Верификация пройдена успешно! Все 8 наборов корректны.")
    else:
        print(f"  Обнаружено ошибок: {errors}")
    print("=" * 50)