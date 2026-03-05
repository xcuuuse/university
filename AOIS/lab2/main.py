import itertools


class LogicalFunctionSolver:
    def __init__(self):
        self.variables = ['x1', 'x2', 'x3']
        self.n_vars = len(self.variables)
        self.truth_table = []
        self.index = 0

    def define_function(self, x1, x2, x3):
        inner = ((not x1) or (not x2)) and (not x2) and x3
        return not inner

    def generate_truth_table(self):
        self.truth_table = []
        print("-" * 30)
        print("Таблица истинности")
        print(f"{'x1':<3} {'x2':<3} {'x3':<3} | {'f(x)':<5} | {'Вес':<5}")
        print("-" * 30)

        binary_values = []
        for j, inputs in enumerate(itertools.product([0, 1], repeat=self.n_vars)):
            x1, x2, x3 = inputs
            result = int(self.define_function(x1, x2, x3))
            weight = 2 ** (7 - j)

            self.truth_table.append({
                'j': j,
                'inputs': inputs,
                'result': result,
                'weight': weight
            })

            binary_values.append(str(result))
            print(f"{x1:<3} {x2:<3} {x3:<3} | {result:<5} | {weight:<5}")
        binary_string = "".join(binary_values)
        self.index = int(binary_string, 2)

        print("-" * 30)
        print(f"Индекс функции i = {self.index}")
        print("-" * 30)

    def get_literal(self, var_name, value):
        if value == 1:
            return var_name
        else:
            return f"!{var_name}"

    def build_sdnf(self):
        terms = []
        indices = []
        for row in self.truth_table:
            if row['result'] == 1:
                indices.append(row['j'])
                term = " * ".join([self.get_literal(v, val) for v, val in zip(self.variables, row['inputs'])])
                terms.append(f"({term})")

        sdnf_str = " v ".join(terms) if terms else "0"
        numeric_form = f"v({', '.join(map(str, indices))})" if indices else "None"
        return sdnf_str, numeric_form, indices

    def build_sknf(self):
        terms = []
        indices = []
        for row in self.truth_table:
            if row['result'] == 0:
                indices.append(row['j'])
                term = " + ".join([self.get_literal(v, 1 - val) for v, val in zip(self.variables, row['inputs'])])
                terms.append(f"({term})")

        sknf_str = " ∧ ".join(terms) if terms else "1"
        numeric_form = f"∧({', '.join(map(str, indices))})" if indices else "None"
        return sknf_str, numeric_form, indices

    def run(self):
        print("Функция: f = !((!x1 + !x2) * !x2 * x3)")

        self.generate_truth_table()

        sdnf_expr, sdnf_num, sdnf_indices = self.build_sdnf()
        sknf_expr, sknf_num, sknf_indices = self.build_sknf()

        print("\nРЕЗУЛЬТАТЫ ПРЕОБРАЗОВАНИЯ:")
        print("=" * 30)

        print("\n1. (СДНФ):")
        print(f"   Аналитическая: {sdnf_expr}")
        print(f"   Числовая форма: {sdnf_num}")

        print("\n2.(СКНФ):")
        print(f"   Аналитическая: {sknf_expr}")
        print(f"   Числовая форма: {sknf_num}")

        print("\n3. Числовой индекс функции:")
        print(f"   i = {self.index}")

        print("\n4. Запись в числовой форме (по методу Мак-Класки / индексная форма):")
        print(f"   f_сднф = {sdnf_num}")
        print(f"   f_скнф = {sknf_num}")
        print("=" * 30)


if __name__ == "__main__":
    solver = LogicalFunctionSolver()
    solver.run()