import shaXX


size_br_attack = 0


def attack(sha_size=16):
    """
    Фугкция находит коллизию используя парадокс
    дней рождений для хэш функций sha16.
    :return: tuple(x, y), где х != y и sha16(x) = sha16(y)
    """
    s = set()
    global size_br_attack
    while True:
        x = shaXX.generate()
        h_x = shaXX.get(x, sha_size)
        for element in s:
            if h_x == element[1]:
                return x, element[0]
        s.add((x, h_x))
        size_br_attack = s.__sizeof__()
