import math
from itertools import combinations
from collections import Counter

VARIANT = 1
NUM_STATES = 8
COUNTER_TYPE = "суммирующий"
BASIS = "НЕ-И-ИЛИ"

n = math.ceil(math.log2(NUM_STATES))
NUM_VARS = n + 1

VAR_NAMES = [f"q{i}*" for i in range(n, 0, -1)] + ["v"]

print("=" * 60)
print(f"Вариант {VARIANT}: Двоичный счётчик {COUNTER_TYPE}ого типа")
print(f"Количество внутренних состояний: {NUM_STATES}")
print(f"Базис: {BASIS}, элемент памяти: T-триггер")
print("=" * 60)

print(f"\n--- Параметры автомата ---")
print(f"Количество элементов памяти (n): n >= log2({NUM_STATES}) = {n}")
print(f"Триггеры: q{n}, ..., q1 (всего {n} шт.)")
print(f"Входной сигнал: V")
print(f"Количество входов КС: W = n + 1 = {NUM_VARS} (автомат Мура, w=0)")
print(f"Выходные сигналы: q{n}..q1 (состояния триггеров)")


def next_state_up(current, v):
    if v == 0:
        return current
    return (current + 1) % NUM_STATES


header_bits = [f"q{i}*" for i in range(n, 0, -1)]
output_bits = [f"q{i}"  for i in range(n, 0, -1)]
excit_bits  = [f"h{i}"  for i in range(n, 0, -1)]
col_w = 4

print(f"\n--- Таблица переходов и возбуждения ---\n")
header_row = "".join(f"{lbl:>{col_w}}" for lbl in header_bits + ["V"] + output_bits + excit_bits)
print(header_row)
print("-" * len(header_row))

rows = []
for state in range(2**n):
    for v in range(2):
        q_prev = [(state >> (n - 1 - i)) & 1 for i in range(n)]
        nxt    = next_state_up(state, v)
        q_next = [(nxt   >> (n - 1 - i)) & 1 for i in range(n)]
        h      = [abs(q_next[i] - q_prev[i]) for i in range(n)]
        row    = q_prev + [v] + q_next + h
        rows.append(row)
        print("".join(f"{x:>{col_w}}" for x in row))


def row_index(row):
    idx = 0
    for b in row[:NUM_VARS]:
        idx = (idx << 1) | b
    return idx


def get_minterms(hi_idx):
    ones, zeros = [], []
    for row in rows:
        h_val = row[n + 1 + n + hi_idx]
        idx   = row_index(row)
        if h_val == 1:
            ones.append(idx)
        else:
            zeros.append(idx)
    return ones, zeros


def int_to_bits(j, n_bits):
    return tuple((j >> (n_bits - 1 - i)) & 1 for i in range(n_bits))


def can_merge(a, b):
    return sum(1 for i in range(len(a)) if a[i] != b[i]) == 1


def merge_terms(a, b):
    return tuple(a[i] if a[i] == b[i] else None for i in range(len(a)))


def quine_mccluskey(ones, n_bits):
    if not ones:
        return []
    groups = {}
    for j in ones:
        bits = int_to_bits(j, n_bits)
        cnt  = sum(b for b in bits)
        groups.setdefault(cnt, set()).add(bits)

    prime_implicants = set()
    while True:
        new_groups    = {}
        merged_in_rnd = set()
        keys = sorted(groups.keys())
        for i in range(len(keys) - 1):
            for a in groups[keys[i]]:
                for b in groups[keys[i + 1]]:
                    if can_merge(a, b):
                        m   = merge_terms(a, b)
                        cnt = sum(bit for bit in m if bit is not None)
                        new_groups.setdefault(cnt, set()).add(m)
                        merged_in_rnd.add(a)
                        merged_in_rnd.add(b)
        for key in groups:
            for term in groups[key]:
                if term not in merged_in_rnd:
                    prime_implicants.add(term)
        if not new_groups:
            break
        groups = new_groups

    def covers(pi, minterm):
        return all(pi[i] is None or pi[i] == minterm[i] for i in range(len(minterm)))

    ones_bits = {int_to_bits(j, n_bits) for j in ones}
    return [pi for pi in prime_implicants if any(covers(pi, m) for m in ones_bits)]


def essential_cover(prime_implicants, ones, n_bits):
    if not prime_implicants or not ones:
        return []
    ones_bits = [int_to_bits(j, n_bits) for j in ones]

    def covers(pi, minterm):
        return all(pi[i] is None or pi[i] == minterm[i] for i in range(len(minterm)))

    coverage  = {m: [pi for pi in prime_implicants if covers(pi, m)] for m in ones_bits}
    selected  = []
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


def implicant_to_str(impl):
    parts = []
    for val, name in zip(impl, VAR_NAMES):
        if val is None:
            continue
        parts.append(name if val == 1 else f"!{name}")
    return " · ".join(parts) if parts else "1"


GRAY = [0b00, 0b01, 0b11, 0b10]


def print_karnaugh(ones_set, zeros_set, func_name):
    nv         = NUM_VARS
    n_row_vars = nv // 2
    n_col_vars = nv - n_row_vars
    n_rows     = 2 ** n_row_vars
    n_cols     = 2 ** n_col_vars
    gray_r     = [i ^ (i >> 1) for i in range(n_rows)]
    gray_c     = [i ^ (i >> 1) for i in range(n_cols)]
    row_header = "".join(VAR_NAMES[:n_row_vars])
    col_header = "".join(VAR_NAMES[n_row_vars:])
    col_labels = [format(g, f'0{n_col_vars}b') for g in gray_c]

    print(f"\n  Карта Вейча-Карно для {func_name}:")
    print(f"  {row_header}\\{col_header} | " + "   ".join(col_labels))
    print("  " + "-" * (len(row_header) + len(col_header) + 6 + 5 * n_cols))
    for rg in gray_r:
        r_label = format(rg, f'0{n_row_vars}b')
        cells = []
        for cg in gray_c:
            idx = (rg << n_col_vars) | cg
            if idx in ones_set:
                cells.append(" 1 ")
            elif idx in zeros_set:
                cells.append(" 0 ")
            else:
                cells.append(" - ")
        print(f"  {r_label:>{len(row_header)+len(col_header)}}     | {'  '.join(cells)}")


print(f"\n--- Минимизация функций возбуждения (Квайн-Мак-Класки + Вейча-Карно) ---")

excit_exprs  = {}
excit_covers = {}

for hi_idx in range(n):
    label       = f"h{n - hi_idx}"
    ones, zeros = get_minterms(hi_idx)
    ones_set    = set(ones)
    zeros_set   = set(zeros)

    print_karnaugh(ones_set, zeros_set, label)

    print(f"\n  {label}:")

    if not ones:
        expr, cover = "0", []
    else:
        pi    = quine_mccluskey(ones, NUM_VARS)
        cover = essential_cover(pi, ones, NUM_VARS)
        terms = [implicant_to_str(p) for p in cover]
        expr  = " v ".join(f"({t})" for t in terms) if terms else "0"

    excit_exprs[label] = expr
    excit_covers[label] = cover
    print(f"    Тупиковая ДНФ: {label} = {expr}")


print(f"\n--- Итоговые выражения возбуждения ---\n")
for label, expr in excit_exprs.items():
    print(f"  {label} = {expr}")


print(f"\n--- Верификация ---\n")


def eval_dnf(cover, bits):
    for impl in cover:
        if all(impl[i] is None or impl[i] == bits[i] for i in range(len(impl))):
            return 1
    return 0


errors = 0
print(f"  {'idx':>4} | входы               | ожид | схема | Статус")
print("  " + "-" * 50)

for row in rows:
    bits_tuple = tuple(row[:NUM_VARS])
    idx        = row_index(row)
    h_expected = row[n + 1 + n:]
    h_calc     = [eval_dnf(excit_covers[f"h{n - hi_idx}"], bits_tuple) for hi_idx in range(n)]
    ok         = h_calc == h_expected
    if not ok:
        errors += 1
    in_str = " ".join(map(str, bits_tuple))
    ex_str = "".join(map(str, h_expected))
    ca_str = "".join(map(str, h_calc))
    status = "OK" if ok else "ОШИБКА"
    print(f"  {idx:>4} | {in_str} | {ex_str:^4} | {ca_str:^5} | {status}")

print()
if errors == 0:
    print("  Верификация пройдена! Все наборы корректны.")
else:
    print(f"  Ошибок: {errors}")


print(f"\n--- Схема автомата ---\n")
print(f"  КС имеет {NUM_VARS} входов: {', '.join(VAR_NAMES)}")
print(f"  КС реализует {n} функции возбуждения T-триггеров:")
for label, expr in excit_exprs.items():
    print(f"    {label} = {expr}")
print(f"\n  Память: {n} T-триггера (T{n}, ..., T1)")
print(f"  Выходы: q{n}(z{n}), ..., q1(z1) — выходной вектор Z")
print(f"\n  При V=0: состояние не меняется (все h=0)")
print(f"  При V=1: счётчик +1 (суммирующий режим)")
print(f"  При переполнении ({NUM_STATES-1} -> 0): все триггеры сбрасываются")
print(f"\n  Схема соединений:")
print(f"    T1 <- h1 = v")
for i in range(2, n + 1):
    chain = " · ".join([f"q{j}*" for j in range(1, i)] + ["v"])
    print(f"    T{i} <- h{i} = {chain}")

print("\n" + "=" * 60)
print("Синтез завершён.")
print("=" * 60)