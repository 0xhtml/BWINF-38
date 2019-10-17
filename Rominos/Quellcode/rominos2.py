import sys
import math


def nachbarn(quadrat, gerade=True):
    """Diese Funktion berechnet die Nachbarn eines Quadrates"""

    # Setzte Richtung (x- o. y-Verschiebung) jenachdem, ob gerade Nachbarn
    # generiert werden sollen
    if gerade:
        richtung = {-1, 0, 1}
    else:
        richtung = {-1, 1}

    # Generiere alle Nachbarn mit Richtung
    nachbarn = {
        (x + quadrat[0], y + quadrat[1])
        for x in richtung
        for y in richtung
    }

    # Filtere alle Nachbarn raus, die im negativem bereich sind.
    nachbarn = filter(lambda x: x[0] >= 0 and x[1] >= 0, nachbarn)

    # Gebe die Nachbarn zurück
    return nachbarn


def nächste(romino, größe):
    """Diese Funktion generiert die nächsten Quadrate für einen Romino"""

    # Teste, ob dies das erstemal Generieren der Quadrate ist
    if len(romino) == 1:
        # Generiere nur diagonale Nachbarn
        nächste = {y for x in romino for y in nachbarn(x, False)}
    else:
        # Generiere diagonale un gerade Nachbarn
        nächste = {y for x in romino for y in nachbarn(x)}

        # Entferne gerade Nachbarn neben der ersten diagonalen Verbindung, damit
        # diese erhalten bleibt
        nächste.remove((romino[0][0], romino[1][1]))
        nächste.remove((romino[1][0], romino[0][1]))

    # Teste, ob dies das letze mal Generieren der Quadrate ist
    if len(romino) == größe - 1:
        # Finde alle Quadrate, für die y=0 gilt
        null = set(filter(lambda x: x[1] == 0, romino))

        # Teste, ob für keine Quadrate y=0 gilt
        if len(null) == 0:
            # Wenn für keine Quadrate y=0 gilt, muss im beim letzten ma
            # Generieren der Quadrate y=0 gelten
            # Filtere alle Quadrate raus, bei denen nicht y=0 gilt
            nächste = filter(lambda x: x[1] == 0, nächste)

    # Filtere alle Quadrate raus, die bereits im Romino vorhanden sind
    nächste = filter(lambda x: x not in romino, nächste)

    # Gib die generierten Quadrate zurück
    return nächste


def gefunden(romino, rominos):
    """Diese Funktion testet, ob ein romino bereits gefunden wurde"""
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
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print("Nutzung:", sys.argv[0], "n ausgabedatei")
        print("   oder:", sys.argv[0], "n")
        sys.exit()

    größe = int(sys.argv[1])
    datei = sys.argv[2] if len(sys.argv) == 3 else None

    print(f"Starte berechnung für n={größe}")

    rominos = [[(0, y)] for y in range(math.floor(größe / 2))]

    for _ in range(größe - 1):
        rominos = [x + [y] for x in rominos for y in nächste(x, größe)]

    rominos = {tuple(sorted(x)) for x in rominos}

    gefilterte_rominos = set()
    for romino in rominos:
        if not gefunden(romino, gefilterte_rominos):
            gefilterte_rominos.add(romino)

    print(f"Es wurden {len(gefilterte_rominos)} Rominos gefunden.")
    if datei is not None:
        datei = datei.split(".")
        datei = ".".join(datei[:-1]) if len(datei) > 1 else datei[0]
        print(f"Speichere Rominos in {datei}.txt ab.")
        datei = open(datei + ".txt", "w")
        datei.write(
            f"{len(gefilterte_rominos)} Rominos der Größe n={größe}\n\n")
        for romino in gefilterte_rominos:
            for x in range(größe):
                for y in range(größe):
                    if (x, y) in romino:
                        datei.write("█")
                    else:
                        datei.write("░")
                datei.write("\n")
            datei.write("\n")
        datei.close()
