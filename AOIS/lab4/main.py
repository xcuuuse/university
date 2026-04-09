
from src.task1 import (build_truth_table,
                       print_truth_table,
                       print_sdnf,
                       print_minimization,
                       multi_output_synthesis,
                       print_circuit_description,
                       verify as verify_task1)
from src.task2 import (build_truth_table as build_truth_table2,
                       print_truth_table as print_truth_table2,
                       print_karnaugh,
                       minimize_all,
                       count_gates,
                       verify as verify_task2)

N = 5


def main():
    table = build_truth_table()
    print_truth_table(table)
    print_sdnf(table)
    print_minimization(table)
    multi_output_synthesis(table)
    print_circuit_description(table)
    verify_task1(table)
    table2 = build_truth_table2(N)
    print_truth_table2(table2, N)

    print("\n  Таблицы Вейча-Карно:")
    for fi, fname in [(4, "y4"), (5, "y3"), (6, "y2"), (7, "y1")]:
        print_karnaugh(table2, fi, fname)

    results = minimize_all(table2)
    count_gates(results)
    verify_task2(table2, results, N)


if __name__ == "__main__":
    main()