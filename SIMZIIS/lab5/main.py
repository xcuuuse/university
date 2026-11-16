import random
import secrets
import hashlib

def is_prime(n, k=40):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def getPrime(bits):
    while True:
        n = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(n):
            return n

def inverse(a, m):
    old_r, r = a, m
    old_s, s = 1, 0
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if old_r != 1:
        raise ValueError("Обратного элемента не существует")
    return old_s % m

def bytes_to_long(b):
    return int.from_bytes(b, 'big')

def long_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8 or 1, 'big')

def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def generate_rsa_keys(bits=1024):
    p = getPrime(bits)
    q = getPrime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = inverse(e, phi)

    return (e, n), (d, n)

def encrypt(message, pub_key):
    e, n = pub_key
    message_int = bytes_to_long(message)
    return mod_exp(message_int, e, n)

def decrypt(ciphertext, priv_key):
    d, n = priv_key
    return long_to_bytes(mod_exp(ciphertext, d, n))

def sign(message, priv_key):
    message_hash = hashlib.sha256(message).digest()
    message_int = bytes_to_long(message_hash)
    d, n = priv_key
    return mod_exp(message_int, d, n)

def verify(message, signature, pub_key):
    message_hash = hashlib.sha256(message).digest()
    message_int = bytes_to_long(message_hash)
    e, n = pub_key
    signature_int = mod_exp(signature, e, n)
    return signature_int == message_int

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# Запись в файл
def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

# Основная программа
def main():
    pub_key, priv_key = generate_rsa_keys(bits=1024)

    # Сохранение ключей в файлы
    write_file('public_key.txt', f'{pub_key[0]} {pub_key[1]}'.encode())
    write_file('private_key.txt', f'{priv_key[0]} {priv_key[1]}'.encode())

    message = read_file('message.txt')

    ciphertext = encrypt(message, pub_key)
    write_file('encrypted_message.txt', str(ciphertext).encode())

    decrypted_message = decrypt(ciphertext, priv_key)
    write_file('decrypted_message.txt', decrypted_message)
    signature = sign(message, priv_key)
    write_file('signature.txt', str(signature).encode())

    is_valid = verify(message, signature, pub_key)
    print(f'{is_valid}')

if __name__ == "__main__":
    main()