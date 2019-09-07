#!/usr/bin/python3
import sys
import itertools
import PIL.Image
import PIL.ImageDraw
import time


class Romino:
    """Ein einzelner Romino bestehend aus n Quadraten"""

    def __init__(self, quadrate):
        # Speichere die ursprüngliche Größe
        self.größe = len(quadrate)

        # Speichere ob dieser Romino bereits verschoben wurde
        self.verschoben = False

        # Speichere die übergebenen Quadrate
        self.quadrate = quadrate

        # Erstelle Dict für desckungsgleiche Rominos
        self.deckungsgleiche = {}

    def verschieben(self):
        """
        Diese Funktion verschiebt die Quadrate eines Rominos an die x- und
        y-Achse.
        +------>
        |
        |  XX
        |   X
        V
        Aus dieser Anordnung z.B. wird die untere Anordnung. (Der Nullpunkt
        beider Achsen befindet sich oben links.)
        +------>
        |XX
        | X
        |
        V
        """
        if not self.verschoben:
            # Ermittle die minimalen X- und Y-Position
            x = self.größe
            y = self.größe
            for quadrat in self.quadrate:
                if quadrat[0] < x:
                    x = quadrat[0]
                if quadrat[1] < y:
                    y = quadrat[1]

            # Verschiebe die Quadrate
            self.quadrate = set(map(lambda q: (q[0] - x, q[1] - y), self.quadrate))
            self.verschoben = True

    def gültig(self):
        """
        Diese Funktion testet, ob es sich um eine gültige Kombination von
        Quadraten handelt.

        Für eine gültige Kombination müssen sich mindestens einmal zwei Quadrate
        nur mit der Ecke (also diagonal) berühren.
        """
        # Teste ob alle Quadrate mit einander verbunden sind
        def verbunden(position, gefunden):
            x, y = position
            o = {(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, 1)}
            for xo, yo in o:
                if len(gefunden) == self.größe:
                    break
                position = (x + xo, y + yo)
                if position in self.quadrate and position not in gefunden:
                    gefunden.add(position)
                    verbunden(position, gefunden)
            return len(gefunden)

        # Suche nach allen verbundenen Quadraten
        erstes_quadrat = self.quadrate.__iter__().__next__()
        verbundene_quadrate = verbunden(erstes_quadrat, {erstes_quadrat})

        # Teste ob alle Quadrate gefunden wurden
        if verbundene_quadrate != self.größe:
            # Es wurden nicht alle Quadrate gefunde. Das heißt, dass nicht
            # alle Quadrate verbuden sind.
            return False

        # Teste ob mindestens eine diagonale Verbindung vorhanden ist:
        # Gehe durch alle Quadrate
        for (x, y) in self.quadrate:
            # Alle diagonalen Positionen
            o = {(-1, -1), (-1, 1), (1, -1), (1, 1)}

            # Gehe durch alle diagonalen Positionen
            for xo, yo in o:
                # Teste ob die diagonale Vorhanden ist und keine gerade
                # Verbindung vorhanden ist
                if (x + xo, y + yo) in self.quadrate and \
                    (x + xo, y) not in self.quadrate and \
                        (x, y + yo) not in self.quadrate:
                    # Es ist eine diagonale Verbindung vorhanden
                    return True

        # Es ist keine diagonale Verbindung vorhanden
        return False

    def spiegeln(self, quadrate, achse):
        max = 0
        for quadrat in quadrate:
            if quadrat[achse] > max:
                max = quadrat[achse]

        funktion = lambda q: q[:achse] + (max - q[achse],) + q[achse + 1:]
        return set(map(funktion, quadrate))

    def achsen_tauschen(self, quadrate):
        return set(map(lambda q: q[::-1], quadrate))

    def deckungsgleich(self, romino):
        """
        Diese Funktion testet ob dieser und ein anderer Romino durch drehen,
        spiegeln und verschieben deckungsgleich sind.
        """
        # Verschiebe die Rominos
        self.verschieben()
        romino.verschieben()

        for achsen_tauschen_bool in [False, True]:
            if achsen_tauschen_bool:
                if (True, 0) in self.deckungsgleiche:
                    achsen_getauscht = self.deckungsgleiche[(True, 0)]
                else:
                    achsen_getauscht = self.achsen_tauschen(self.quadrate)
                    self.deckungsgleiche[(True, 0)] = achsen_getauscht
            else:
                achsen_getauscht = self.quadrate
            if romino.quadrate == achsen_getauscht:
                return True

            if (achsen_tauschen_bool, 1) in self.deckungsgleiche:
                gespiegelt = self.deckungsgleiche[(achsen_tauschen_bool, 1)]
            else:
                gespiegelt = self.spiegeln(achsen_getauscht, 0)
                self.deckungsgleiche[(achsen_tauschen_bool, 1)] = gespiegelt
            if romino.quadrate == gespiegelt:
                return True

            if (achsen_tauschen_bool, 2) in self.deckungsgleiche:
                gespiegelt = self.deckungsgleiche[(achsen_tauschen_bool, 2)]
            else:
                gespiegelt = self.spiegeln(gespiegelt, 1)
                self.deckungsgleiche[(achsen_tauschen_bool, 2)] = gespiegelt
            if romino.quadrate == gespiegelt:
                return True

            if (achsen_tauschen_bool, 3) in self.deckungsgleiche:
                gespiegelt = self.deckungsgleiche[(achsen_tauschen_bool, 3)]
            else:
                gespiegelt = self.spiegeln(achsen_getauscht, 1)
                self.deckungsgleiche[(achsen_tauschen_bool, 3)] = gespiegelt
            if romino.quadrate == gespiegelt:
                return True
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
    mögliche_quadrate = set()
    for x in range(n):
        for y in range(n):
            mögliche_quadrate.add((x, y))

    # Generiere alle möglichen Rominos
    mögliche_rominos = itertools.combinations(mögliche_quadrate, n)

    # Teste alle möglichen Rominos auf Gültigkeit
    gültige_rominos = set()
    for romino_quadrate in mögliche_rominos:
        # Erstelle Romino
        romino = Romino(set(romino_quadrate))

        # Teste Gültigkeit des Romino
        if romino.gültig():
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
