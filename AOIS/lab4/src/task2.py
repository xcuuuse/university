N = 5


def build_truth_table(n):
    table = []
    for j in range(16):
        x4 = (j >> 3) & 1
        x3 = (j >> 2) & 1
        x2 = (j >> 1) & 1
        x1 = (j >> 0) & 1

        if j <= 9:
            out = (j + n) % 16
            y4 = (out >> 3) & 1
            y3 = (out >> 2) & 1
            y2 = (out >> 1) & 1
            y1 = (out >> 0) & 1
            defined = True
        else:
            y4 = y3 = y2 = y1 = None
            defined = False

        table.append((x4, x3, x2, x1, y4, y3, y2, y1, defined))
    return table


def print_truth_table(table, n):
    print("\n" + "=" * 60)
    print(f"  ТАБЛИЦА ИСТИННОСТИ  (8421 → 8421+{n})")
    print("=" * 60)
    print("  J  | x4 x3 x2 x1 | y4 y3 y2 y1 | Определён?")
    print("-" * 55)
    for j, row in enumerate(table):
        x4, x3, x2, x1, y4, y3, y2, y1, defined = row
        if defined:
            ys = f"  {y4}  {y3}  {y2}  {y1}"
            d = "да"
        else:
            ys = "  -  -  -  -"
            d = "нет (избыточный)"
        print(f"  {j:2d} |  {x4}  {x3}  {x2}  {x1} | {ys} | {d}")
    print("=" * 60)


GRAY = [0b00, 0b01, 0b11, 0b10]


def karnaugh_index(row_gray, col_gray):
    x4 = (row_gray >> 1) & 1
    x3 = (row_gray >> 0) & 1
    x2 = (col_gray >> 1) & 1
    x1 = (col_gray >> 0) & 1
    return (x4 << 3) | (x3 << 2) | (x2 << 1) | x1


def print_karnaugh(table, func_idx, func_name):
    print(f"\n  Таблица Вейча-Карно для {func_name}:")
    print(f"  x4x3\\x2x1 | 00  01  11  10")
    print("  " + "-" * 30)
    for rg in GRAY:
        x4 = (rg >> 1) & 1
        x3 = (rg >> 0) & 1
        cells = []
        for cg in GRAY:
            j = karnaugh_index(rg, cg)
            val = table[j][func_idx]
            cells.append(" - " if val is None else f"  {val} ")
        print(f"    {x4}{x3}      | {'|'.join(cells)}")


def int_to_bits(j, n_bits=4):
    return tuple((j >> (n_bits - 1 - i)) & 1 for i in range(n_bits))


def can_merge(a, b):
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    return len(diff) == 1


def merge(a, b):
    return tuple(a[i] if a[i] == b[i] else None for i in range(len(a)))


def quine_mccluskey_dc(ones, dont_cares):
    if not ones:
        return []

    all_terms = list(ones) + list(dont_cares)
    groups = {}
    for j in all_terms:
        bits = int_to_bits(j)
        ones_count = sum(b for b in bits)
        groups.setdefault(ones_count, set()).add(bits)

    prime_implicants = set()

    while True:
        new_groups = {}
        merged_in_round = set()
        keys = sorted(groups.keys())

        for i in range(len(keys) - 1):
            for a in groups[keys[i]]:
                for b in groups[keys[i + 1]]:
                    if can_merge(a, b):
                        m = merge(a, b)
                        ones_in_m = sum(bit for bit in m if bit is not None)
                        new_groups.setdefault(ones_in_m, set()).add(m)
                        merged_in_round.add(a)
                        merged_in_round.add(b)

        for key in groups:
            for term in groups[key]:
                if term not in merged_in_round:
                    prime_implicants.add(term)

        if not new_groups:
            break
        groups = new_groups

    ones_bits = {int_to_bits(j) for j in ones}

    def covers(pi, minterm):
        return all(pi[i] is None or pi[i] == minterm[i] for i in range(len(minterm)))

    result = [pi for pi in prime_implicants
              if any(covers(pi, m) for m in ones_bits)]
    return result


def essential_cover(prime_implicants, ones):
    ones_bits = [int_to_bits(j) for j in ones]

    def covers(pi, minterm):
        return all(pi[i] is None or pi[i] == minterm[i] for i in range(len(minterm)))

    if not prime_implicants or not ones_bits:
        return []

    coverage = {m: [pi for pi in prime_implicants if covers(pi, m)]
                for m in ones_bits}

    selected = []
    uncovered = set(ones_bits)

    for m, pis in coverage.items():
        if len(pis) == 1 and pis[0] not in selected:
            selected.append(pis[0])

    for pi in selected:
        uncovered = {m for m in uncovered if not covers(pi, m)}

    remaining = [p for p in prime_implicants if p not in selected]
    while uncovered and remaining:
        best = max(remaining, key=lambda pi: sum(1 for m in uncovered if covers(pi, m)))
        selected.append(best)
        remaining.remove(best)
        uncovered = {m for m in uncovered if not covers(best, m)}

    return selected


VAR_NAMES = ("x4", "x3", "x2", "x1")


def implicant_to_str_dnf(impl):
    parts = []
    for val, name in zip(impl, VAR_NAMES):
        if val is None:
            continue
        parts.append(name if val == 1 else f"!{name}")
    return "(" + " * ".join(parts) + ")" if parts else "1"


def implicant_to_str_knf(impl):
    # В КНФ: скобка — дизъюнкт; переменная входит без инверсии если val==0,
    # с инверсией (!x) если val==1
    parts = []
    for val, name in zip(impl, VAR_NAMES):
        if val is None:
            continue
        parts.append(f"!{name}" if val == 1 else name)
    return "(" + " ∨ ".join(parts) + ")" if parts else "0"


def minimize_all(table):
    defined_ones = {fi: [] for fi in range(4, 8)}
    defined_zeros = {fi: [] for fi in range(4, 8)}
    dont_cares = []

    for j, row in enumerate(table):
        if not row[8]:
            dont_cares.append(j)
        else:
            for fi in range(4, 8):
                if row[fi] == 1:
                    defined_ones[fi].append(j)
                else:
                    defined_zeros[fi].append(j)

    results = {}
    func_names = {4: "y4", 5: "y3", 6: "y2", 7: "y1"}

    print("\n" + "=" * 60)
    print("  МИНИМИЗАЦИЯ ФУНКЦИЙ (Квайн–МакКласки + избыточные)")
    print("=" * 60)

    for fi in range(4, 8):
        fname = func_names[fi]
        ones = defined_ones[fi]
        zeros = defined_zeros[fi]

        print(f"\n  {fname}:")
        print(f"    Единицы (1): наборы {ones}")
        print(f"    Нули    (0): наборы {zeros}")
        print(f"    Избыточные:  наборы {dont_cares}")

        if not ones:
            print(f"    Результат: {fname} = 0")
            results[fname] = ("dnf", [], "0")
            continue

        if not zeros:
            print(f"    Результат: {fname} = 1")
            results[fname] = ("dnf", [], "1")
            continue

        pi_dnf = quine_mccluskey_dc(ones, dont_cares)
        cover_dnf = essential_cover(pi_dnf, ones)
        expr_dnf = " v ".join(implicant_to_str_dnf(p) for p in cover_dnf) if cover_dnf else "0"

        pi_knf = quine_mccluskey_dc(zeros, dont_cares)
        cover_knf = essential_cover(pi_knf, zeros)
        expr_knf = " * ".join(implicant_to_str_knf(p) for p in cover_knf) if cover_knf else "1"

        # Выбираем форму с меньшим числом термов
        if len(cover_knf) < len(cover_dnf):
            print(f"    ТДНФ: {fname} = {expr_dnf}")
            print(f"    ТКНФ: {fname} = {expr_knf}  <- выбрана (короче)")
            results[fname] = ("knf", cover_knf, expr_knf)
        else:
            print(f"    ТДНФ: {fname} = {expr_dnf}  <- выбрана (не длиннее КНФ)")
            print(f"    ТКНФ: {fname} = {expr_knf}")
            results[fname] = ("dnf", cover_dnf, expr_dnf)

    return results


def count_gates(results):
    print("\n" + "=" * 60)
    print("  ОЦЕНКА ОБОРУДОВАНИЯ")
    print("=" * 60)

    inverters_needed = set()
    and_gates = []
    or_gates = []

    for fname, data in results.items():
        form = data[0]
        cover = data[1]
        expr = data[2]
        print(f"\n  {fname} ({form.upper()}): {expr}")

        for impl in cover:
            for val, name in zip(impl, VAR_NAMES):
                if val is None:
                    continue
                # ДНФ: инвертор нужен для val==0 (нужна !x)
                # КНФ: инвертор нужен для val==1 (нужна !x в дизъюнкте)
                if form == "dnf" and val == 0:
                    inverters_needed.add(name)
                elif form == "knf" and val == 1:
                    inverters_needed.add(name)

            n_inputs = sum(1 for v in impl if v is not None)
            if n_inputs >= 2:
                if form == "dnf":
                    and_gates.append(n_inputs)
                else:
                    or_gates.append(n_inputs)

        if len(cover) >= 2:
            if form == "dnf":
                or_gates.append(len(cover))
            else:
                and_gates.append(len(cover))

    print(f"\n  Инверторов (НЕ): {len(inverters_needed)} — {sorted(inverters_needed)}")

    from collections import Counter
    and_count = Counter(and_gates)
    or_count = Counter(or_gates)

    for n_in, cnt in sorted(and_count.items()):
        print(f"  Элементов И  на {n_in} входа: {cnt}")
    for n_in, cnt in sorted(or_count.items()):
        print(f"  Элементов ИЛИ на {n_in} входа: {cnt}")

    # Приближённый подсчёт транзисторов (КМОП: НЕ=2, И/ИЛИ ≈ 2*n)
    transistors = len(inverters_needed) * 2
    for n_in in and_gates:
        transistors += 2 * n_in
    for n_in in or_gates:
        transistors += 2 * n_in
    print(f"\n  Ориентировочно транзисторов: ~{transistors}")


def verify(table, results, n):
    print("\n" + "=" * 60)
    print("  ВЕРИФИКАЦИЯ")
    print("=" * 60)

    func_names = ["y4", "y3", "y2", "y1"]

    def eval_dnf(cover, bits_dict):
        for impl in cover:
            term = True
            for val, name in zip(impl, VAR_NAMES):
                if val is None:
                    continue
                term = term and (bits_dict[name] == val)
            if term:
                return 1
        return 0

    def eval_knf(cover, bits_dict):
        for impl in cover:
            clause = False
            for val, name in zip(impl, VAR_NAMES):
                if val is None:
                    continue
                # В КНФ val==0 → x входит прямо; clause=True если x==1 (т.е. x != 0)
                # val==1 → !x входит; clause=True если x==0 (т.е. x != 1)
                clause = clause or (bits_dict[name] != val)
            if not clause:
                return 0
        return 1

    errors = 0
    print(f"  {'J':>3} | x4x3x2x1 | y4y3y2y1(ожид) | y4y3y2y1(схема) | Статус")
    print("  " + "-" * 65)

    for j, row in enumerate(table):
        x4, x3, x2, x1, ey4, ey3, ey2, ey1, defined = row
        if not defined:
            continue

        bits = {"x4": x4, "x3": x3, "x2": x2, "x1": x1}
        calc = []
        for fname in func_names:
            data = results[fname]
            form, cover = data[0], data[1]
            if form == "dnf":
                calc.append(eval_dnf(cover, bits))
            else:
                calc.append(eval_knf(cover, bits))

        expected = [ey4, ey3, ey2, ey1]
        ok = calc == expected
        if not ok:
            errors += 1
        status = "OK" if ok else "ОШИБКА"
        exp_str = "".join(map(str, expected))
        calc_str = "".join(map(str, calc))
        print(f"  {j:>3} |  {x4} {x3} {x2} {x1}   |   {exp_str}          |   {calc_str}           | {status}")

    print()
    if errors == 0:
        print("  Верификация пройдена! Все определённые наборы корректны.")
    else:
        print(f"  Ошибок: {errors}")
    print("=" * 60)
