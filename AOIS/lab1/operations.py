from codes import to_direct, to_additional, to_invert


def operations_direct(value1: int, value2: int, bits: int):
    return to_direct(value1 + value2, bits)


def operations_additional(value1: int, value2: int, bits: int):
    a_dk = to_additional(value1, bits)
    b_dk = to_additional(value2, bits)

    sum_value = int(a_dk, 2) + int(b_dk, 2)
    result_dk = format(sum_value & ((1 << bits) - 1), f'0{bits}b')
    return result_dk


def operations_inverted(value1: int, value2: int, bits: int):
    a_ok = to_invert(value1, bits)
    b_ok = to_invert(value2, bits)

    sum_value = int(a_ok, 2) + int(b_ok, 2)

    carry = sum_value >> bits

    result_ok = format(sum_value & ((1 << bits) - 1), f'0{bits}b')

    if carry:
        result_ok = format((int(result_ok, 2) + carry) & ((1 << bits) - 1), f'0{bits}b')

    return result_ok


def multiply_direct(value1: int, value2: int, bits: int):
    return to_direct(value1 * value2, bits + 1)


def multiply_additional(value1: int, value2: int, bits: int):
    return to_additional(value1 * value2, bits + 1)


def divide_modules(dividend: int, divisor: int, fractional_bits: int = 5) -> str:
    if divisor == 0:
        raise ZeroDivisionError("Деление на ноль невозможно")
    integer_part = dividend // divisor
    remainder = dividend % divisor
    integer_bin = bin(integer_part)[2:] if integer_part > 0 else '0'

    fractional_digits = []
    current_remainder = remainder

    for _ in range(fractional_bits + 1):
        current_remainder *= 2
        if current_remainder >= divisor:
            fractional_digits.append('1')
            current_remainder -= divisor
        else:
            fractional_digits.append('0')

    if fractional_digits[-1] == '1':
        main_digits = fractional_digits[:-1]
        carry = 1
        for i in range(len(main_digits) - 1, -1, -1):
            if carry == 0:
                break
            if main_digits[i] == '0':
                main_digits[i] = '1'
                carry = 0
            else:
                main_digits[i] = '0'
                carry = 1

        fractional_str = ''.join(main_digits)

        if carry == 1:
            integer_part += 1
            integer_bin = bin(integer_part)[2:]
            fractional_str = '0' * fractional_bits
    else:
        fractional_str = ''.join(fractional_digits[:-1])
    return f"{integer_bin}.{fractional_str}"


def add_floating_point_task4(mantissa1: int, mantissa2: int) -> dict:
    order1 = int("100", 2)
    order2 = int("101", 2)

    if order1 > order2:
        shift = order1 - order2
        aligned_m1 = mantissa1
        aligned_m2 = mantissa2 >> shift
        result_order = order1
    else:
        shift = order2 - order1
        aligned_m1 = mantissa1 >> shift
        aligned_m2 = mantissa2
        result_order = order2

    mantissa_sum = aligned_m1 + aligned_m2

    normalization_shift = 0
    while mantissa_sum >= (1 << 7):
        mantissa_sum >>= 1
        result_order += 1
        normalization_shift += 1

    return {
        "mantissa1": mantissa1,
        "mantissa2": mantissa2,
        "order1": order1,
        "order2": order2,
        "aligned_mantissa1": aligned_m1,
        "aligned_mantissa2": aligned_m2,
        "mantissa_sum": to_direct(mantissa_sum, 8),
        "result_order": to_direct(result_order, 4),
        "normalization_shift": normalization_shift,
        "result_value": mantissa_sum
    }