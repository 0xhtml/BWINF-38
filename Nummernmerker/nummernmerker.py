import sys
import itertools
import math


def generiere_blöcke(nummer, blocklängen):
    """Generiere die Blöcke mit den Blocklängen"""

    # Erstelle Variable für die Blöcke
    blöcke = []

    # Gehe durch alle Blocklängen
    for blocklänge in blocklängen:
        # Füge den Teil der Nummer als neune Block hinzu
        blöcke.append(nummer[:blocklänge])

        # Entferne den Teil von der Nummer
        nummer = nummer[blocklänge:]

    # Gebe die Blöcke zurück
    return blöcke


def generiere_mögliche_blocklängen(nummer):
    """Genereire die möglichen Kombinationen für Längen der Blöcke"""

    # Berechne die max- und minimale Blockanzahl
    maximale_block_anzahl = math.floor(len(nummer) / 2)
    minimale_block_anzahl = math.ceil(len(nummer) / 4)

    # Finde alle Kombinationen
    mögliche_blocklängen = set()

    # Gehe durch alle möglichen Blockanzahlen
    for block_anzahl in range(minimale_block_anzahl, maximale_block_anzahl + 1):
        # Generiere alle Kombinationen der Längen (2, 3 u. 4)
        block_längen = [[2, 3, 4] for _ in range(block_anzahl)]
        mögliche_blocklängen.update(itertools.product(*block_längen))

    # Sortiere alle Längen aus, bei die summiert Länger oder Kürzer als die
    # Nummer sind
    mögliche_blocklängen = filter(lambda x: sum(
        x) == len(nummer), mögliche_blocklängen)

    # Gebe die möglichen Blocklängen
    return mögliche_blocklängen


def generiere_mögliche_blöcke(nummer, mögliche_blocklängen):
    """Generiere die möglichen Blöcke"""

    # Erstelle Veriable für die möglichen Blöcke
    mögliche_blöcke = []

    # Gehe durch alle Blocklängen
    for blocklänge in mögliche_blocklängen:
        # Füge die Blöcke mit der Blocklänge hinzu
        mögliche_blöcke.append(generiere_blöcke(nummer, blocklänge))

    # Gebe die möglichen Blöcke zurück
    return mögliche_blöcke


def zähle_nullen_am_anfang(blöcke):
    """Zählt die Anzahl der Blöcke, die mit Null beginnen"""

    # Erstelle Variable für die Anzahl
    anzahl = 0

    # Gehe durch alle Blöcke
    for block in blöcke:
        # Wenn der Block mit Null beginnt, erhöhe die Anzahl um 1
        if block[0] == "0":
            anzahl += 1

    # Gebe die Anzahl zurück
    return anzahl


def beste_blöcke(mögliche_blöcke):
    """Finde die besten Blöcke (wenigste Nullen und möglichst wenig Blöcke)"""

    # Erstelle Variablen für die besten Blöcke und deren Nullen und Blockanzahl
    beste_nullen = math.inf
    beste_anzahl = math.inf
    beste_blöcke = None

    # Gehe durch alle möglichen Blöcke
    for blöcke in mögliche_blöcke:
        # Zähle die Nullen am Anfang
        nullen = zähle_nullen_am_anfang(blöcke)

        # Wenn die Blöcke weniger Nullen am Anfang haben, sind diese besser,
        # speichere diese also ab
        if nullen < beste_nullen:
            beste_nullen = nullen
            beste_anzahl = len(blöcke)
            beste_blöcke = blöcke
        # Wenn die Blöcke gleichviele Nullen am Anfang haben, sind diese besser,
        # speichere diese also auch ab
        elif nullen == beste_nullen and len(blöcke) < beste_anzahl:
            beste_anzahl = len(blöcke)
            beste_blöcke = blöcke

    # Gebe die besten Blöcke zurück
    return beste_blöcke


if __name__ == "__main__":
    # Wenn nicht alle Argumente angegeben wurden, gebe Informationen zu den
    # benötigten Argument aus und beende das Programm
    if len(sys.argv) != 2:
        print("Benutzung:", sys.argv[0], "nummer")
        sys.exit()

    # Generiere alle möglichen kombinationen von Block längen
    mögliche_blocklängen = generiere_mögliche_blocklängen(sys.argv[1])

    # Generiere alle Blöcke mit den möglichen Block längen
    mögliche_blöcke = generiere_mögliche_blöcke(sys.argv[1], mögliche_blocklängen)

    # Finden die beste Möglichkeit für die Unterteilung in Blöcke
    beste_blöcke = beste_blöcke(mögliche_blöcke)

    # Gebe die besten Blöcke aus
    print("\n".join(beste_blöcke))
