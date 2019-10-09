import time
import math

count = 0


def mögliche_telepaartien(verteilung):
    res = set()

    for a in range(len(verteilung)):
        for b in range(len(verteilung)):
            if a != b and (b, a) not in res:
                res.add((a, b))

    return res


def telepaartiere(verteilung, a, b):
    if verteilung[a] < verteilung[b]:
        a, b = b, a
    verteilung[a] -= verteilung[b]
    verteilung[b] += verteilung[b]
    return verteilung


def run(verteilung, tiefe):
    global count
    count += 1
    if 0 in verteilung:
        return [verteilung]
    if tiefe == 0:
        return False

    telepaartien = mögliche_telepaartien(verteilung)

    best = False
    bestlen = math.inf

    for telepaartie in telepaartien:
        telepaartierte_verteilung = telepaartiere(verteilung[:], *telepaartie)
        res = run(telepaartierte_verteilung, tiefe - 1)
        if res != False and len(res) < bestlen:
            best = [telepaartie] + res
            bestlen = len(res)
            tiefe = len(res)

    return best


if __name__ == "__main__":
    startzeit = time.time()

    verteilung = [2, 4, 9]
    res = run(verteilung, 100)

    if res != False:
        print(res)
    print(count)
    print("%.0f" % ((time.time() - startzeit) * 1000), "ms")
