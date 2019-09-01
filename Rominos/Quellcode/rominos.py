#!./env/bin/python3
import sys
import itertools
import numpy
import PIL.Image
import PIL.ImageDraw


class Romino:
    """Ein einzelner Romino bestehend aus n Quadraten"""

    def __init__(self, n):
        self.array = numpy.zeros((n, n))

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

    def deckungsgleich(self, array1, array2=None, rotation=0):
        """
        Diese Funktion testet ob zwei Rominos durch drehen, spiegeln und
        verschieben deckungsgleich sind.
        """
        if rotation == 4:
            return False

        if array2 is None:
            array2 = self.array

        # Rotiere den zweiten Romino
        rotierte_array2 = numpy.rot90(array2)

        # Verschiebe Rominos an den Nullpunkt
        min_x1 = len(array1)
        min_y1 = len(array1)
        min_x2 = len(array1)
        min_y2 = len(array1)
        for x in range(len(array1)):
            for y in range(len(array1)):
                if array1[x][y] == 1:
                    min_x1 = min(x, min_x1)
                    min_y1 = min(y, min_y1)
                if rotierte_array2[x][y] == 1:
                    min_x2 = min(x, min_x2)
                    min_y2 = min(y, min_y2)
        verschobene_array1 = numpy.roll(numpy.roll(
            array1, -min_x1, axis=0), -min_y1, axis=1)
        verschobene_array2 = numpy.roll(numpy.roll(
            rotierte_array2, -min_x2, axis=0), -min_y2, axis=1)

        return (verschobene_array1 == verschobene_array2).all() or \
            (verschobene_array1 == numpy.flip(verschobene_array2, 0)).all() or \
            (verschobene_array1 == numpy.flip(verschobene_array2, 1)).all() or \
            self.deckungsgleich(verschobene_array1,
                                verschobene_array2, rotation + 1)

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
                        [(x2 * 10 + x, y2 * 10 + y), (x2 * 10 + 10 + x, y2 * 10 + 10 + y)],
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
    bild = PIL.Image.new("RGB", ((n + 1) * 10 * größe - 9, (n + 1) * 10 * größe - 9))
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
    bild.save(sys.argv[2])
