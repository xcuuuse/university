def to_direct(value: int, bits: int) -> str:
    if value >= 0:
        return format(value, f'0{bits}b')
    return '1' + format(abs(value), f'0{bits - 1}b')


def to_invert(value: int, bits: int) -> str:
    if value >= 0:
        return format(value, f'0{bits}b')
    direct = format(abs(value), f'0{bits-1}b')
    ans = ''.join('1' if b == '0' else '0' for b in direct)
    return '1' + ans


def to_additional(value: int, bits: int) -> str:
    if value >= 0:
        return format(value, f'0{bits}b')
    return format((1 << bits) + value, f'0{bits}b')
