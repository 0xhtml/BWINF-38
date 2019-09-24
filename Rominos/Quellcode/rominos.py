#!/usr/bin/python3
import sys
import itertools
import PIL.Image
import PIL.ImageDraw
import time


def gültig(quadrate):
    """
    Diese Funktion testet, ob es sich um eine gültige Kombination von
    Quadraten handelt.

    Für eine gültige Kombination müssen alle Quadrate verbunden sein und sich
    mindestens einmal zwei Quadrate nur mit der Ecke (also diagonal) berühren.
    """
    # Teste ob alle Quadrate mit einander verbunden sind
    erstes_quadrat = quadrate.__iter__().__next__()
    gefunden = set()
    nächste = {erstes_quadrat}

    while len(nächste) > 0:
        nachbarn = set()
        for quadrat in nächste:
            for xo, yo in {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}:
                position = (quadrat[0] + xo, quadrat[1] + yo)
                if position in quadrate and position not in gefunden:
                    nachbarn.add(position)
        gefunden.update(nächste)
        nächste = nachbarn

    if len(gefunden) != len(quadrate):
        return False

    # Teste ob mindestens eine diagonale Verbindung vorhanden ist:
    # Gehe durch alle Quadrate
    for (x, y) in quadrate:
        # Alle diagonalen Positionen
        o = {(-1, -1), (-1, 1), (1, -1), (1, 1)}

        # Gehe durch alle diagonalen Positionen
        for xo, yo in o:
            # Teste ob die diagonale Vorhanden ist und keine gerade
            # Verbindung vorhanden ist
            if (x + xo, y + yo) in quadrate and \
                (x + xo, y) not in quadrate and \
                    (x, y + yo) not in quadrate:
                # Es ist eine diagonale Verbindung vorhanden
                return True

    # Es ist keine diagonale Verbindung vorhanden
    return False


class Romino:
    """Ein einzelner Romino bestehend aus n Quadraten"""

    def __init__(self, quadrate):
        # Speichere die ursprüngliche Größe
        self.größe = len(quadrate)

        # Speichere ob dieser Romino bereits verschoben wurde
        self.verschoben = False

        # Ermittle die minimalen X- und Y-Position
        x = self.größe
        y = self.größe
        for quadrat in quadrate:
            if quadrat[0] < x:
                x = quadrat[0]
            if quadrat[1] < y:
                y = quadrat[1]

        # Verschiebe die Quadrate
        def funktion(q): return (q[0] - x, q[1] - y)
        self.quadrate = set(map(funktion, quadrate))

        # Erstelle Dict für desckungsgleiche Rominos
        self.deckungsgleiche = {}

    def spiegeln(self, quadrate, achse):
        max = 0
        for quadrat in quadrate:
            if quadrat[achse] > max:
                max = quadrat[achse]

        def funktion(q): return q[:achse] + (max - q[achse],) + q[achse + 1:]
        return set(map(funktion, quadrate))

    def achsen_tauschen(self, quadrate):
        return set(map(lambda q: q[::-1], quadrate))

    def deckungsgleich(self, romino):
        """
        Diese Funktion testet ob dieser und ein anderer Romino durch drehen,
        spiegeln und verschieben deckungsgleich sind.
        """
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        for quadrat in self.quadrate:
            if quadrat[0] > x1:
                x1 = quadrat[0]
            if quadrat[1] > y1:
                y1 = quadrat[1]
        for quadrat in romino.quadrate:
            if quadrat[0] > x2:
                x2 = quadrat[0]
            if quadrat[1] > y2:
                y2 = quadrat[1]

        if x1 == x2 and y1 == y2 and x1 == y1:
            achsen_tauschen_bools = [False, True]
        elif x1 == x2 and y1 == y2:
            achsen_tauschen_bools = [False]
        elif x1 == y2 and y1 == x2:
            achsen_tauschen_bools = [True]
        else:
            return False

        for achsen_tauschen_bool in achsen_tauschen_bools:
            if achsen_tauschen_bool:
                if (True, 0) in self.deckungsgleiche:
                    quadrate = self.deckungsgleiche[(True, 0)]
                else:
                    quadrate = self.achsen_tauschen(self.quadrate)
                    self.deckungsgleiche[(True, 0)] = quadrate
            else:
                quadrate = self.quadrate

            if quadrate == romino.quadrate:
                return True

            i = 1
            for spiegelachse in [0, 1, 0]:
                if (achsen_tauschen_bool, i) in self.deckungsgleiche:
                    quadrate = self.deckungsgleiche[(achsen_tauschen_bool, i)]
                else:
                    quadrate = self.spiegeln(quadrate, spiegelachse)
                    self.deckungsgleiche[(achsen_tauschen_bool, i)] = quadrate
                if quadrate == romino.quadrate:
                    return True
                i += 1
        return False

    def render(self, draw, x, y):
        draw.rectangle(
            [(x, y), (x + self.größe * 10, y + self.größe * 10)],
            None,
            (100, 100, 100)
        )
        for quadrat in self.quadrate:
            draw.rectangle(
                [(quadrat[0] * 10 + x, quadrat[1] * 10 + y),
                    (quadrat[0] * 10 + 10 + x, quadrat[1] * 10 + 10 + y)],
                (0xcf, 0x2b, 0x1d),
                (0, 0, 0)
            )


if __name__ == "__main__":
    start = time.time()

    if len(sys.argv) != 3:
        # Es wurden nicht alle Argumente angegeben
        print("Benutzung:", sys.argv[0], "n ausgabedateiname")
        exit()

    try:
        n = int(sys.argv[1])
    except ValueError:
        # Die angegebene Anzahl ist keine Zahl
        print("Die Anzahl der zu verwendenen Quadrate muss eine Zahl sein")
        exit()

    # Generiere alle möglichen Quadrat positionen
    mögliche_quadrate = itertools.product(range(n), range(n))

    # Generiere alle möglichen Rominos
    mögliche_rominos = itertools.combinations(mögliche_quadrate, n)

    # Teste alle möglichen Rominos auf Gültigkeit
    mögliche_rominos = filter(gültig, mögliche_rominos)
    mögliche_rominos = map(Romino, mögliche_rominos)
    gültige_rominos = set()
    for romino in mögliche_rominos:
        for romino2 in gültige_rominos:
            if romino.deckungsgleich(romino2):
                break
        else:
            gültige_rominos.add(romino)

    # Speichere Rominos ab
    größe = 1
    while größe * größe < len(gültige_rominos):
        größe += 1
    bild = PIL.Image.new(
        "RGB", ((n + 1) * 10 * größe - 9, (n + 1) * 10 * größe - 9))
    draw = PIL.ImageDraw.Draw(bild)
    draw.rectangle((0, 0) + bild.size, (255, 255, 255))
    x = 0
    y = 0
    for romino in gültige_rominos:
        romino.render(draw, (n + 1) * 10 * x, (n + 1) * 10 * y)
        x += 1
        if x >= größe:
            x = 0
            y += 1
    draw.text((1, bild.height-10), str(len(gültige_rominos)), (0, 0, 0))
    bild.save(sys.argv[2])

    print(time.time() - start, "s")
