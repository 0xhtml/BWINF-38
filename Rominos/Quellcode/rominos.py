#!/usr/bin/python3
import sys
import itertools
import numpy
import PIL.Image
import PIL.ImageDraw


class Romino:
    """Ein einzelner Romino bestehend aus n Quadraten"""

    def __init__(self, array):
        # Speichere die ursprüngliche Größe
        self.größe = len(array)

        # Speichere ob dieser Romino bereits verschoben wurde
        self.verschoben = False

        # Speichere die übergebenen Quadrate
        self.array = array

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
            # Ermittle die mini- und maximalen X- und Y-Position
            min_x = array.shape[0]
            min_y = array.shape[1]
            max_x = 0
            max_y = 0
            for x in range(array.shape[0]):
                for y in range(array.shape[1]):
                    if array[x][y] == 0:
                        continue

                    if x < min_x:
                        min_x = x
                    if y < min_y:
                        min_y = y
                    if x > max_x:
                        max_x = x
                    if y > max_y:
                        max_y = y

            # Entferne alles bis and die mini- und maximalen Positionen
            self.array = array[min_x:max_x + 1, min_y:max_y + 1]
            self.verschoben = True

    def gültig(self):
        """
        Diese Funktion testet, ob es sich um eine gültige Kombination von
        Quadraten handelt.

        Für eine gültige Kombination müssen sich mindestens einmal zwei Quadrate
        nur mit der Ecke (also diagonal) berühren.
        """
        # Teste ob alle Quadrate mit einander verbunden sind
        gefunden = set()
        for x in range(self.array.shape[0]):
            for y in range(self.array.shape[1]):
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
                        gefunden.add((x, y))
                    else:
                        return False

        # Teste ob mindestens eine diagonale Verbindung vorhanden ist
        for x, y in gefunden:
            if (x + 1, y + 1) in gefunden and \
                (x + 1, y) not in gefunden and \
                    (x, y + 1) not in gefunden:
                return True
            if (x + 1, y - 1) in gefunden and \
                (x + 1, y) not in gefunden and \
                    (x, y - 1) not in gefunden:
                return True
            if (x - 1, y + 1) in gefunden and \
                (x - 1, y) not in gefunden and \
                    (x, y + 1) not in gefunden:
                return True
            if (x - 1, y - 1) in gefunden and \
                (x - 1, y) not in gefunden and \
                    (x, y - 1) not in gefunden:
                return True
        return False

    def gleich(self, array):
        """Diese Funktion testet ob zwei Rominos gleich sind."""
        return self.array.shape == array.shape and (self.array == array).all()

    def deckungsgleich(self, romino):
        """
        Diese Funktion testet ob dieser und ein anderer Romino durch drehen,
        spiegeln und verschieben deckungsgleich sind.
        """
        # Verschiebe die Rominos
        self.verschieben()
        romino.verschieben()

        # Lade den Romino
        array = self.array

        # Lade bereits gespeicherte rotiert/gepsiegelte Rominos
        gespeichert = self.deckungsgleiche.keys()

        # Gehe durch alle Rotationen
        rotationen = (0, 1, 2, 3)
        for rotation in rotationen:
            # Rotiere den Romino
            if (rotation, False) in gespeichert:
                array = self.deckungsgleiche[(rotation, False)]
            else:
                if rotation != 0:
                    array = numpy.rot90(array)

                    # Speichere den rotierten Romino ab
                    self.deckungsgleiche[(rotation, False)] = array

            # Gehe durch alle Spiegelungen
            for spiegeln in (True, False):
                # Teste ob der Romino gespiegelt werden soll
                if spiegeln:
                    if (rotation, True) in gespeichert:
                        gespiegeltes_array = self.deckungsgleiche[(
                            rotation, True)]
                    else:
                        # Spiegel den Romino
                        gespiegeltes_array = numpy.flip(array, 1)

                        # Speichere den gespiegelten Romino ab
                        self.deckungsgleiche[(
                            rotation, True)] = gespiegeltes_array
                else:
                    gespiegeltes_array = array

                # Vergleiche die beiden Rominos
                if romino.gleich(gespiegeltes_array):
                    return True
        return False

    def render(self, draw, x, y):
        draw.rectangle(
            [(x, y), (x + self.größe * 10, y + self.größe * 10)],
            None,
            (100, 100, 100)
        )
        for x2 in range(self.array.shape[0]):
            for y2 in range(self.array.shape[1]):
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
    mögliche_quadrate = set()
    for x in range(n):
        for y in range(n):
            mögliche_quadrate.add((x, y))

    # Generiere alle möglichen Rominos
    mögliche_rominos = itertools.combinations(mögliche_quadrate, n)

    # Teste alle möglichen Rominos auf Gültigkeit
    gültige_rominos = set()
    for romino_quadrate in mögliche_rominos:
        # Erstelle leeren Romino
        array = numpy.zeros((n, n))

        # Füge Quadrate zu Romino hinzu
        for quadrat in romino_quadrate:
            array[quadrat] = 1

        # Erstelle Romino
        romino = Romino(array)

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
