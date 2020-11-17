from hashlib import sha256
import os


bytesize = 8
table = {0: 255, 1: 128, 2: 192, 3: 224, 4: 240, 5: 248, 6: 252, 7: 254}


def okr(num):
    """
    num: округляемое число
    :return: минимальное челое число >= num/8
    """
    if num/bytesize > num//bytesize:
        return num//bytesize + 1
    return num//bytesize


def generate(dim=3):
    """
    Генерация случайного вектора байт размера dim
    """
    return os.urandom(dim)


def get(msg, res_size=16):
    """
    Функция получает хеш от элемента key с помощью хеш-функции
    SHA256, затем возвращает первые 16 бит от результата SHA256
    msg: хешируемый элемент
    blocksize: размер выхода SHA256 в байтах
    res_size: размер результата фукнции в байтах
    """
    if not isinstance(msg, (bytes, bytearray)):
        raise TypeError("key: expected bytes or bytearray, but got {}".format(type(msg).__name__))
    dig = sha256(msg).digest()[:3]
    result = b''
    for i in range(okr(res_size)):
        it = dig[i]
        if i == okr(res_size) - 1:
            it &= table[res_size - bytesize * (res_size // bytesize)]
        result += it.to_bytes(1, byteorder="big")
    return result

#print(get(bytes.fromhex('00f27690'), 20), get(bytes.fromhex('00871f90'), 20))