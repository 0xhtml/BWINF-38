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
        Diese Funktion testet, ob es sich um eine gültige Kombinatzion von
        Quadraten handelt.

        Für eine gültige Kombination müssen sich mindestens einmal zwei Quadrate
        nur mit der Ecke (also diagonal) berühren.
        """
        diagonalen = False
        # Gehe durch alle Positionen
        for i in range(len(self.array)):
            for j in range(len(self.array)):
                # Überspringe Positionen, auf denen kein Quadrat ist
                if self.array[i][j] == 0:
                    continue

                # Teste ob das Quadrat die anderen Quadrate berührt
                berührt = False
                for xo in [-1, 1]:
                    for yo in [-1, 1]:
                        try:
                            if self.array[x+xo][y+yo] == 1:
                                berührt = True
                                break
                        except IndexError:
                            pass
                    if berührt:
                        break
                if not berührt:
                    return False

                if diagonalen:
                    continue
                # Teste ob diagonal zu der Position sich mindestens ein Quadrat
                # befindet.
                try:
                    # Rechts-Oben
                    if self.array[i+1][j+1] == 1 and self.array[i+1][j] == 0 and self.array[i][j+1] == 0:
                        diagonalen = True
                except IndexError:
                    pass
                try:
                    # Rechts-Unten
                    if self.array[i+1][j-1] == 1 and self.array[i+1][j] == 0 and self.array[i][j-1] == 0:
                        diagonalen = True
                except IndexError:
                    pass
                try:
                    # Links-Oben
                    if self.array[i-1][j+1] == 1 and self.array[i-1][j] == 0 and self.array[i][j+1] == 0:
                        diagonalen = True
                except IndexError:
                    pass
                try:
                    # Links-Unten
                    if self.array[i-1][j-1] == 1 and self.array[i-1][j] == 0 and self.array[i][j-1] == 0:
                        diagonalen = True
                except IndexError:
                    pass
        return diagonalen

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

        return (verschobene_array1 == rotierte_array2).all() or \
            (verschobene_array1 == numpy.flip(rotierte_array2, 0)).all() or \
            (verschobene_array1 == numpy.flip(rotierte_array2, 1)).all() or \
            self.deckungsgleich(verschobene_array1, rotierte_array2, rotation + 1)

    def render(self):
        bild = PIL.Image.new(
            "RGB", (len(self.array) * 10, len(self.array) * 10))
        draw = PIL.ImageDraw.Draw(bild)
        for x in range(len(self.array)):
            for y in range(len(self.array)):
                if self.array[x][y] == 1:
                    draw.rectangle(
                        [(x * 10, y * 10), (x * 10 + 10, y * 10 + 10)],
                        (255, 255, 255)
                    )
        return bild


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
                romino.render().save("save" + str(len(gültige_rominos)) + ".png")
                gültige_rominos.append(romino)

    # Speichere Rominos ab
    print(len(gültige_rominos))
