import sys
import time
import math


def nachbarn(q):
    nachbarn = {-1, 0, 1}
    nachbarn = {(x + q[0], y + q[1]) for x in nachbarn for y in nachbarn}
    nachbarn = filter(lambda x: x[0] >= 0 and x[1] >= 0, nachbarn)
    return nachbarn


def diagonal(romino):
    for quadrat in romino:
        for x, y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if (quadrat[0] + x, quadrat[1] + y) in romino and \
                (quadrat[0], quadrat[1] + y) not in romino and \
                    (quadrat[0] + x, quadrat[1]) not in romino:
                return True
    return False


def nächste(romino_anfang):
    nächste = {y for x in romino_anfang for y in nachbarn(x)}
    def a(x): return x not in romino_anfang
    def b(x): return romino_anfang + [x] == sorted(romino_anfang + [x])
    nächste = filter(lambda x: a(x) and b(x), nächste)
    return nächste


def an_null(romino):
    x = False
    y = False
    for quadrat in romino:
        if quadrat[0] == 0:
            x = True
        if quadrat[1] == 0:
            y = True
    return x and y


def gefunden(romino, rominos):
    spiegelungen = [(x, y, z) for x in range(2)
                    for y in range(2) for z in range(2)]
    for spiegelung in spiegelungen:
        gespiegelt = romino
        if spiegelung[0]:
            max_x = 0
            for quadrat in romino:
                if quadrat[0] > max_x:
                    max_x = quadrat[0]
            gespiegelt = [(max_x - x[0], x[1]) for x in gespiegelt]
        if spiegelung[1]:
            max_y = 0
            for quadrat in romino:
                if quadrat[1] > max_y:
                    max_y = quadrat[1]
            gespiegelt = [(x[0], max_y - x[1]) for x in gespiegelt]
        if spiegelung[2]:
            gespiegelt = [x[::-1] for x in gespiegelt]
        gespiegelt.sort()
        if gespiegelt in rominos:
            return True
    return False


if __name__ == "__main__":
    start_zeit = time.time()

    if len(sys.argv) != 3:
        print("Nutzung:", sys.argv[0], "n ausgabedatei")
        exit()

    n = int(sys.argv[1])
    ausgabedatei = sys.argv[2]

    rominos = [[(0, y)] for y in range(math.floor(n / 2))]

    for _ in range(n - 1):
        rominos = [x + [y] for x in rominos for y in nächste(x)]

    rominos = filter(lambda x: diagonal(x) and an_null(x), rominos)

    gefilterte_rominos = []
    for romino in rominos:
        if not gefunden(romino, gefilterte_rominos):
            gefilterte_rominos.append(romino)

    print(len(gefilterte_rominos))

    print("%.0f" % ((time.time() - start_zeit) * 1000), "ms")
