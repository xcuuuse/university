import itertools

VARS = ['x1', 'x2', 'x3']
N = len(VARS)


def eval_function(x1, x2, x3) -> int:
    inner = ((not x1) or (not x2)) and not((not x2) and x3)
    return int(not inner)


def build_truth_table():
    return [{'j': j, 'vals': combo, 'f': eval_function(*combo)}
            for j, combo in enumerate(itertools.product([0, 1], repeat=N))]


def term_to_str(term, dnf):
    parts = [VARS[i] if t == 1 else f"!{VARS[i]}" for i, t in enumerate(term) if t != -1]
    if not parts:
        return "1" if dnf else "0"
    return (" * " if dnf else " + ").join(parts)


def form_str(terms, dnf):
    joiner = " + " if dnf else " * "
    parts = [term_to_str(t, dnf) if dnf else f"({term_to_str(t, dnf)})" for t in terms]
    return joiner.join(parts) if parts else ("0" if dnf else "1")


def build_form(table, dnf):
    target = 1 if dnf else 0
    return [tuple(v if dnf else 1-v for v in r['vals']) for r in table if r['f'] == target]


def try_glue(a, b):
    diff = [i for i in range(N) if a[i] != b[i]]
    if len(diff) != 1: return None
    r = list(a); r[diff[0]] = -1
    return tuple(r)


def quine_reduce(terms):
    cur = list(set(terms))
    while True:
        used, nxt = set(), []
        for i in range(len(cur)):
            for j in range(i+1, len(cur)):
                g = try_glue(cur[i], cur[j])
                if g is not None:
                    used |= {i, j}
                    if g not in nxt: nxt.append(g)
        for i, t in enumerate(cur):
            if i not in used and t not in nxt: nxt.append(t)
        if nxt == cur: break
        cur = nxt
    return cur


def covers(impl, const):
    return all(impl[i] == -1 or impl[i] == const[i] for i in range(N))


def remove_redundant(implicants, constituents):
    res = list(implicants)
    changed = True
    while changed:
        changed = False
        for cand in res[:]:
            others = [t for t in res if t != cand]
            if all(any(covers(o, c) for o in others) for c in constituents if covers(cand, c)):
                res.remove(cand); changed = True; break
    return res


def calc_method(terms, consts, dnf, label):
    print(f"\n{'='*50}\n  РАСЧЁТНЫЙ МЕТОД — {label}\n{'='*50}")
    reduced = quine_reduce(terms)
    print(f"  Шаг 1 — Сокращённая форма: {form_str(reduced, dnf)}")
    print("  Шаг 2 — Проверка лишних:")
    for cand in reduced:
        others = [t for t in reduced if t != cand]
        redundant = all(any(covers(o, c) for o in others) for c in consts if covers(cand, c))
        print(f"    {term_to_str(cand, dnf):<20} -> {'ЛИШНЯЯ' if redundant else 'нелишняя'}")
    dead = remove_redundant(reduced, consts)
    print(f"  Тупиковая форма: {form_str(dead, dnf)}")
    return dead


def quine_mccluskey(terms, consts, dnf, label):
    print(f"\n{'='*50}\n  МЕТОД КВАЙНА-МАК-КЛАСКИ — {label}\n{'='*50}")
    reduced = quine_reduce(terms)
    print(f"  Шаг 1 — Сокращённая форма: {form_str(reduced, dnf)}")
    print("\n  Шаг 2 — Таблица покрытия:")
    W = 22
    print(f"  {'Импликанта':<20}" + "".join(f"{term_to_str(c, dnf):<{W}}" for c in consts))
    print("  " + "-" * (20 + W * len(consts)))
    for imp in reduced:
        row = f"  {term_to_str(imp, dnf):<20}"
        row += "".join(f"{'X' if covers(imp, c) else ' ':<{W}}" for c in consts)
        print(row)
    dead = remove_redundant(reduced, consts)
    redundant = [imp for imp in reduced if imp not in dead]
    print(f"  Лишние: {', '.join(term_to_str(i, dnf) for i in redundant) or 'нет'}")
    print(f"  Тупиковая форма: {form_str(dead, dnf)}")
    return dead


GRAY_COLS = [(0,0),(0,1),(1,1),(1,0)]


def karnaugh_method(table, terms, consts, dnf, label):
    print(f"\n{'='*50}\n  МЕТОД КАРНО — {label}\n{'='*50}")
    cells = {r['vals']: r['f'] for r in table}
    target = 1 if dnf else 0
    print(f"  Карта Карно ({'единицы' if dnf else 'нули'}):")
    print(f"  {'x1\\x2x3':<10}" + "".join(f"  {x2}{x3}" for x2,x3 in GRAY_COLS))
    print("  " + "-"*26)
    for x1 in [0,1]:
        print(f"  {x1:<10}" + "".join(f"  {cells[(x1,x2,x3)]} " for x2,x3 in GRAY_COLS))

    target_cells = {k for k,v in cells.items() if v == target}
    all_groups = []
    for mask in itertools.product([-1,0,1], repeat=3):
        grp = {(x1,x2,x3) for x1 in [0,1] for x2,x3 in GRAY_COLS
               if all(mask[i]==-1 or mask[i]==(x1,x2,x3)[i] for i in range(3))}
        if grp and grp <= target_cells and len(grp) in (1,2,4,8):
            all_groups.append((mask, grp))
    all_groups.sort(key=lambda g: -len(g[1]))

    covered, chosen = set(), []
    for mask, grp in all_groups:
        if grp - covered:
            chosen.append(mask); covered |= grp
        if covered == target_cells: break

    implicants = []
    for mask in chosen:
        term = tuple(-1 if m==-1 else (1-m if not dnf else m) for m in mask)
        implicants.append(term)

    dead = remove_redundant(implicants, consts)
    print(f"\n  Группы: {', '.join(term_to_str(i, dnf) for i in implicants)}")
    print(f"  Тупиковая форма: {form_str(dead, dnf)}")
    return dead


def tdnf_to_tknf(dnf_terms):
    result = [()]
    for conj in dnf_terms:
        lits = [(i,v) for i,v in enumerate(conj) if v != -1]
        new = []
        for existing in result:
            for (i,v) in lits:
                nc = list(existing)
                skip = False
                for (ei,ev) in existing:
                    if ei == i:
                        if ev != v: skip = True
                        break
                else:
                    nc.append((i,v))
                if not skip:
                    nc_s = sorted(nc, key=lambda x: x[0])
                    if nc_s not in new: new.append(nc_s)
        result = new
    knf = []
    for clause in result:
        term = [-1]*N
        for i,v in clause: term[i] = v
        knf.append(tuple(term))
    return [t1 for i,t1 in enumerate(knf)
            if not any(all(t2[k]==-1 or t2[k]==t1[k] for k in range(N)) and t2!=t1
                       for j,t2 in enumerate(knf) if i!=j)]


def main():
    print("Функция: f = !((!x1 + !x2) * !(!x2 * x3))")
    table = build_truth_table()
    print("\nТаблица истинности")
    print(f"{'j':<3} {'x1':<4} {'x2':<4} {'x3':<4} | f\n" + "-"*35)
    for r in table:
        print(f"{r['j']:<3} {r['vals'][0]:<4} {r['vals'][1]:<4} {r['vals'][2]:<4} | {r['f']}")
    binary_str = "".join(str(r['f']) for r in table)
    print(f"\nИндекс: {int(binary_str,2)}  ({binary_str})\n" + "-"*35)

    sdnf = build_form(table, dnf=True)
    sknf = build_form(table, dnf=False)
    print(f"\nСДНФ: {form_str(sdnf, True)}")
    print(f"СКНФ: {form_str(sknf, False)}")
    print("\n МИНИМИЗАЦИЯ СДНФ\n")
    r1d = calc_method(sdnf, sdnf, True, "СДНФ")
    r2d = quine_mccluskey(sdnf, sdnf, True, "СДНФ")
    r3d = karnaugh_method(table, sdnf, sdnf, True, "СДНФ")
    print("\n МИНИМИЗАЦИЯ СКНФ\n")
    r1k = calc_method(sknf, sknf, False, "СКНФ")
    r2k = quine_mccluskey(sknf, sknf, False, "СКНФ")
    r3k = karnaugh_method(table, sknf, sknf, False, "СКНФ")

    print(f"\n{'='*50}\n  СРАВНЕНИЕ ТРЁХ МЕТОДОВ\n{'='*50}")
    labels = ["Расчётный", "Квайн-Мак-Класки", "Карно"]
    ok = True
    for name, results, dnf in [("ТДНФ", [r1d,r2d,r3d], True), ("ТКНФ", [r1k,r2k,r3k], False)]:
        print(f"  {name}:")
        for lbl, res in zip(labels, results):
            print(f"    {lbl:<22}: {form_str(res, dnf)}")
        if all(set(results[0]) == set(r) for r in results):
            print(f"Все методы совпали")
        else:
            print(f"РАЗЛИЧАЮТСЯ!"); ok = False

    print(f"\n  СРАВНЕНИЕ ТДНФ И ТКНФ\n")
    converted = tdnf_to_tknf(r1d)
    reduced = remove_redundant(converted, sknf)
    print(f"  ТДНФ:              {form_str(r1d, True)}")
    print(f"  ТКНФ:              {form_str(r1k, False)}")
    print(f"  ТДНФ -> КНФ:        {form_str(converted, False)}")
    print(f"  После упрощения:   {form_str(reduced, False)}")
    match = set(reduced) == set(r1k)
    print(f"  {'ТДНФ == ТКНФ' if match else 'НЕ СОВПАЛИ'}")

    print(f"\nИТОГ\n")
    print(f"  ТДНФ: {form_str(r1d, True)}")
    print(f"  ТКНФ: {form_str(r1k, False)}")
    print(f"  Три метода: {'СОВПАЛИ' if ok else 'НЕ СОВПАЛИ'}")


if __name__ == "__main__":
    main()