import sys
import time


def nachbarn(quadrat):
    nachbarn = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
    nachbarn = [(x + quadrat[0], y + quadrat[1]) for x, y in nachbarn]
    def a(x): return x[0] >= 0 and x[1] >= 0
    def b(x): return x[0] < n and x[1] < n
    nachbarn = filter(lambda x: a(x) and b(x), nachbarn)
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
    nächste = [x for x in nachbarn(romino_anfang[-1])]
    def a(x): return x not in romino_anfang
    def b(x): return diagonal(romino_anfang + [x])
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

    rominos = [[(x, y)] for x in range(n) for y in range(n)]
    def a(x): return sum(x[0]) < n / 2 + 1
    def b(x): return x[0][0] == 0 or x[0][1] == 0
    rominos = filter(lambda x: a(x) and b(x), rominos)

    for _ in range(n - 1):
        rominos = [x + [y] for x in rominos for y in nächste(x)]

    rominos = filter(an_null, rominos)

    gefilterte_rominos = []
    for romino in rominos:
        if not gefunden(romino, gefilterte_rominos):
            gefilterte_rominos.append(romino)

    print(gefilterte_rominos[:5])
    print(len(gefilterte_rominos))

    print("%.0f" % ((time.time() - start_zeit) * 1000), "ms")
