#!/usr/bin/python3
import sys
import itertools
import numpy
import PIL.Image
import PIL.ImageDraw


class Romino:
    """Ein einzelner Romino bestehend aus n Quadraten"""

    def __init__(self, n):
        self.array = numpy.zeros((n, n))
        self.deckungsgleiche = {}

    def add(self, x, y):
        self.array[x][y] = 1

    def gültig(self):
        """
        Diese Funktion testet, ob es sich um eine gültige Kombination von
        Quadraten handelt.

        Für eine gültige Kombination müssen sich mindestens einmal zwei Quadrate
        nur mit der Ecke (also diagonal) berühren.
        """
        # Teste ob alle Quadrate mit einander verbunden sind
        gefunden = []
        for x in range(len(self.array)):
            for y in range(len(self.array)):
                if self.array[x][y] == 1:
                    if (x+1, y+1) in gefunden or \
                            (x+1, y) in gefunden or \
                            (x+1, y-1) in gefunden or \
                            (x, y+1) in gefunden or \
                            (x, y-1) in gefunden or \
                            (x-1, y+1) in gefunden or \
                            (x-1, y) in gefunden or \
                            (x-1, y-1) in gefunden or \
                            len(gefunden) == 0:
                        gefunden.append((x, y))
                    else:
                        return False

        # Teste ob mindestens eine diagonale Verbindung vorhanden ist
        for x, y in gefunden:
            if (x + 1, y + 1) in gefunden and (x + 1, y) not in gefunden and (x, y + 1) not in gefunden:
                return True
            if (x + 1, y - 1) in gefunden and (x + 1, y) not in gefunden and (x, y - 1) not in gefunden:
                return True
            if (x - 1, y + 1) in gefunden and (x - 1, y) not in gefunden and (x, y + 1) not in gefunden:
                return True
            if (x - 1, y - 1) in gefunden and (x - 1, y) not in gefunden and (x, y - 1) not in gefunden:
                return True
        return False

    @staticmethod
    def verschieben(array):
        min_x = array.shape[0]
        min_y = array.shape[1]
        max_x = 0
        max_y = 0

        for x in range(array.shape[0]):
            for y in range(array.shape[1]):
                if array[x][y] == 0:
                    continue

                min_x = min(x, min_x)
                min_y = min(y, min_y)
                max_x = max(x, max_x)
                max_y = max(y, max_y)

        return array[min_x:max_x + 1, min_y:max_y + 1]

    def gleich(self, array1, array2, rotation=0, spiegeln=False):
        size = len(array1)

        if rotation != 0:
            array1 = numpy.rot90(array1, rotation)
        if spiegeln:
            array1 = numpy.flip(array1, 1)

        ergebnis = array1.shape == array2.shape and (array1 == array2).all()
        return ergebnis, array1

    def deckungsgleich(self, array):
        """
        Diese Funktion testet ob zwei Rominos durch drehen, spiegeln und
        verschieben deckungsgleich sind.
        """
        array1 = self.verschieben(self.array)
        array2 = self.verschieben(array)

        rotationen = (0, 1, 2, 3)
        for rotation in rotationen:
            for spiegeln in [True, False]:
                if (rotation, spiegeln) in self.deckungsgleiche.keys():
                    array3 = self.deckungsgleiche[(rotation, spiegeln)]
                    if self.gleich(array3, array2)[0]:
                        return True
                else:
                    gleich, array3 = self.gleich(
                        array1, array2, rotation, spiegeln)
                    self.deckungsgleiche[(rotation, spiegeln)] = array3
                    if gleich:
                        return True
        return False

    def render(self, draw, x, y):
        draw.rectangle(
            [(x, y), (x + len(self.array) * 10, y + len(self.array) * 10)],
            None,
            (100, 100, 100)
        )
        for x2 in range(len(self.array)):
            for y2 in range(len(self.array)):
                if self.array[x2][y2] == 1:
                    draw.rectangle(
                        [(x2 * 10 + x, y2 * 10 + y),
                         (x2 * 10 + 10 + x, y2 * 10 + 10 + y)],
                        (0xcf, 0x2b, 0x1d),
                        (0, 0, 0)
                    )


if __name__ == "__main__":
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
    mögliche_quadrate = []
    for x in range(n):
        for y in range(n):
            mögliche_quadrate.append((x, y))

    # Generiere alle möglichen Rominos
    mögliche_rominos = itertools.combinations(mögliche_quadrate, n)

    # Teste alle möglichen Rominos auf Gültigkeit
    gültige_rominos = []
    for romino_quadrate in mögliche_rominos:
        # Erstelle neuen Romino
        romino = Romino(n)

        # Füge Quadrate zu Romino hinzu
        for quadrat in romino_quadrate:
            romino.add(*quadrat)

        # Teste Gültigkeit des Romino
        if romino.gültig():
            for romino2 in gültige_rominos:
                if romino.deckungsgleich(romino2.array):
                    break
            else:
                gültige_rominos.append(romino)

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
