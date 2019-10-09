import sys
import time


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
    if 0 in verteilung:
        return [verteilung]
    if tiefe == 0:
        return False

    telepaartien = mögliche_telepaartien(verteilung)

    bester = False

    for telepaartie in telepaartien:
        telepaartierte_verteilung = telepaartiere(verteilung[:], *telepaartie)
        res = run(telepaartierte_verteilung, tiefe - 1)
        if res != False and (bester == False or len(res) < len(bester)):
            bester = [telepaartie] + res
            tiefe = len(res)

    return bester


if __name__ == "__main__":
    startzeit = time.time()

    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("Benutzung:", sys.argv[0], "n")
        print("      oder", sys.argv[0], "behälter1 behälter2 behälter3")
        exit()

    if len(sys.argv) == 2:
        n = int(sys.argv[1])

        verteilungen = []
        for a in range(1, n):
            for b in range(1, n - a):
                verteilungen.append([a, b, n - a - b])

        bester = []
        for verteilung in verteilungen:
            telepaartieschritte = run(verteilung, n)
            if len(telepaartieschritte) - 1 > len(bester) - 2:
                bester = telepaartieschritte + [verteilung]

        print(len(bester) - 2)
    else:
        b1 = int(sys.argv[1])
        b2 = int(sys.argv[2])
        b3 = int(sys.argv[3])
        verteilung = [b1, b2, b3]

        telepaartieschritte = run(verteilung, 50)
        for telepaartie in telepaartieschritte[:-1]:
            a = str(verteilung)
            verteilung = telepaartiere(verteilung, *telepaartie)
            c = str(verteilung)

            b = "  " + str(telepaartie[0] + 1) + " <"
            b += "-" * (len(a) - len(b) * 2)
            b += "> " + str(telepaartie[1] + 1)

            print(a)
            print(b)
            print(c)
            print()

        print(len(telepaartieschritte) - 1, "Schritte")
