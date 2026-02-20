from codes import to_direct, to_additional, to_invert
from operations import operations_direct, operations_additional, operations_inverted,\
    divide_modules, add_floating_point_task4, multiply_additional, multiply_direct


def show_direct(value1: int, value2: int, bits: int):
    print("Представление десятичного числа в прямом коде: ")
    print(f"{value1}₁₀ == {to_direct(value1, bits)}₂")
    print(f"-{value1}₁₀ == {to_direct(-value1, bits)}₂")
    print(f"{value2}₁₀ == {to_direct(value2, bits)}₂")
    print(f"-{value2}₁₀ == {to_direct(-value2, bits)}₂")


def show_inverted(value1: int, value2: int, bits: int):
    print("Представление десятичного числа в обратном коде: ")
    print(f"{value1}₁₀ == {to_invert(value1, bits)}₂")
    print(f"-{value1}₁₀ == {to_invert(-value1, bits)}₂")
    print(f"{value2}₁₀ == {to_invert(value2, bits)}₂")
    print(f"-{value2}₁₀ == {to_invert(-value2, bits)}₂")


def show_additional(value1: int, value2: int, bits: int):
    print("Представление десятичного числа в дополнительном коде: ")
    print(f"{value1}₁₀ == {to_additional(value1, bits)}₂")
    print(f"-{value1}₁₀ == {to_additional(-value1, bits)}₂")
    print(f"{value2}₁₀ == {to_additional(value2, bits)}₂")
    print(f"-{value2}₁₀ == {to_additional(-value2, bits)}₂")


def main():
    x1_abs = 11
    x2_abs = 21
    bits = 8
    combinations = [
        (x1_abs, x2_abs),
        (x1_abs, -x2_abs),
        (-x1_abs, x2_abs),
        (-x1_abs, -x2_abs)
    ]
    show_direct(x1_abs, x2_abs, bits)
    show_inverted(x1_abs, x2_abs, bits)
    show_additional(x1_abs, x2_abs, bits)
    print("ЗАДАНИЕ 1: Сложение/вычитание в разных кодах")
    for a, b in combinations:
        print(f"\nОперация: ({a}) + ({b})")
        print(f"Прямой код:   {operations_direct(a, b, bits)}")
        print(f"Обратный код: {operations_inverted(a, b, bits)}")
        print(f"Доп. код:     {operations_additional(a, b, bits)}")

    print("\n\nЗАДАНИЕ 2: Умножение модулей")
    product_direct = multiply_direct(x1_abs, x2_abs, bits)
    product_additional = multiply_additional(x1_abs, x2_abs, bits)
    print(f"Модули: {x1_abs} × {x2_abs} = {x1_abs * x2_abs}")

    signs = [('+', '+'), ('+', '-'), ('-', '+'), ('-', '-')]
    print("\nЗнаки произведения:")
    for sa, sb in signs:
        sign = '0' if sa == sb else '1'
        print(f"{sign}{to_direct(x1_abs * x2_abs, bits)}")

    print("\n\nЗАДАНИЕ 3: Деление модулей")
    division_result = divide_modules(x1_abs, x2_abs)
    print(f"Модули: {x1_abs} / {x2_abs} = {division_result}₂")

    print("\nЗнаки частного:")
    for sa, sb in signs:
        sign = '0' if sa == sb else '1'
        print(f"{sign} {division_result}")

    print("\n\nЗАДАНИЕ 4: Сложение чисел с плавающей точкой")
    fp_result = add_floating_point_task4(x1_abs, x2_abs)
    print(f"M1 = {fp_result['mantissa1']}, P1 = {fp_result['order1']}")
    print(f"M2 = {fp_result['mantissa2']}, P2 = {fp_result['order2']}")
    print(f"Результат: 0.{fp_result['mantissa_sum']} × 2^{fp_result['result_order']} = {fp_result['result_value']}₁₀")


if __name__ == "__main__":
    main()

