import src.task1 as task1
import src.task2 as task2
N = 5


def main():
    var_names = ("X1", "X2", "X3")

    table = task1.build_truth_table()
    task1.print_truth_table(table)

    task1.print_sdnf(table, var_names)

    task1.print_minimization(table, var_names)

    task1.multi_output_synthesis(table, var_names)

    task1.print_circuit_description(table)

    task1.verify(table)

    n = N
    table = task2.build_truth_table(n)
    task2.print_truth_table(table, n)

    print("\n" + "=" * 60)
    print("  КАРТЫ КАРНО")
    print("=" * 60)
    for fi, fname in zip(range(4, 8), ["y4", "y3", "y2", "y1"]):
        task2.print_karnaugh(table, fi, fname)

    results = task2.minimize_all(table)
    
    print("\n" + "=" * 60)
    print("  ИТОГОВЫЕ МИНИМИЗИРОВАННЫЕ ФОРМУЛЫ")
    print("=" * 60)
    for fname in ["y4", "y3", "y2", "y1"]:
        data = results[fname]
        print(f"  {fname} = {data[2]}")

    task2.count_gates(results)

    task2.verify(table, results, n)


if __name__ == "__main__":
    main()
