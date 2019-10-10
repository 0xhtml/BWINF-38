import sys
import time
import math


def nachbarn(q, nachbarn):
    nachbarn = {(x + q[0], y + q[1]) for x in nachbarn for y in nachbarn}
    nachbarn = filter(lambda x: x[0] >= 0 and x[1] >= 0, nachbarn)
    return nachbarn


def nächste(romino_anfang, n):
    if len(romino_anfang) == 1:
        nächste = {y for x in romino_anfang for y in nachbarn(x, {-1, 1})}
    else:
        nächste = {y for x in romino_anfang for y in nachbarn(x, {-1, 0, 1})}
        nächste.remove((romino_anfang[0][0], romino_anfang[1][1]))
        nächste.remove((romino_anfang[1][0], romino_anfang[0][1]))

    if len(romino_anfang) == n - 1:
        null = set(filter(lambda x: x[1] == 0, romino_anfang))
        if len(null) == 0:
            nächste = filter(lambda x: x[1] == 0, nächste)

    nächste = filter(lambda x: x not in romino_anfang, nächste)
    return nächste


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
        gespiegelt = tuple(sorted(gespiegelt))
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
        rominos = [x + [y] for x in rominos for y in nächste(x, n)]

    rominos = {tuple(sorted(x)) for x in rominos}

    gefilterte_rominos = []
    for romino in rominos:
        if not gefunden(romino, gefilterte_rominos):
            gefilterte_rominos.append(romino)

    print(len(gefilterte_rominos))

    print("%.0f" % ((time.time() - start_zeit) * 1000), "ms")
