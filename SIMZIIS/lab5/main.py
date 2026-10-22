import random
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
import hashlib

# Функция для последовательного возведения в квадрат и умножения
def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# Генерация ключей RSA
def generate_rsa_keys(bits=1024):
    p = getPrime(bits)
    q = getPrime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Открытая экспонента
    e = 65537
    # Секретная экспонента
    d = inverse(e, phi)

    return (e, n), (d, n)

# Шифрование сообщения
def encrypt(message, pub_key):
    e, n = pub_key
    message_int = bytes_to_long(message)
    return mod_exp(message_int, e, n)

# Расшифровка сообщения
def decrypt(ciphertext, priv_key):
    d, n = priv_key
    return long_to_bytes(mod_exp(ciphertext, d, n))

# Цифровая подпись
def sign(message, priv_key):
    message_hash = hashlib.sha256(message).digest()
    message_int = bytes_to_long(message_hash)
    d, n = priv_key
    return mod_exp(message_int, d, n)

# Проверка подписи
def verify(message, signature, pub_key):
    message_hash = hashlib.sha256(message).digest()
    message_int = bytes_to_long(message_hash)
    e, n = pub_key
    signature_int = mod_exp(signature, e, n)
    return signature_int == message_int

# Чтение из файла
def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# Запись в файл
def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

# Основная программа
def main():
    # Генерация ключей
    pub_key, priv_key = generate_rsa_keys(bits=1024)

    # Сохранение ключей в файлы
    write_file('public_key.txt', f'{pub_key[0]} {pub_key[1]}'.encode())
    write_file('private_key.txt', f'{priv_key[0]} {priv_key[1]}'.encode())

    # Чтение исходного сообщения``
    message = read_file('message.txt')

    # Шифрование
    ciphertext = encrypt(message, pub_key)
    write_file('encrypted_message.txt', str(ciphertext).encode())

    # Расшифровка
    decrypted_message = decrypt(ciphertext, priv_key)
    write_file('decrypted_message.txt', decrypted_message)

    # Подпись
    signature = sign(message, priv_key)
    write_file('signature.txt', str(signature).encode())

    # Проверка подписи
    is_valid = verify(message, signature, pub_key)
    print(f'Подпись действительна: {is_valid}')

if __name__ == "__main__":
    main()