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


def nächste(romino, größe, auf_halbe_größe):
    """Diese Funktion generiert die nächsten Quadrate für einen Romino"""

    # Teste, ob dies das erstemal Generieren der Quadrate ist
    if len(romino) == 1:
        # Generiere nur diagonale Nachbarn
        nächste = {y for x in romino[-auf_halbe_größe:] for y in nachbarn(x, 0)}
    else:
        # Generiere diagonale un gerade Nachbarn
        nächste = {y for x in romino[-auf_halbe_größe:] for y in nachbarn(x)}

        # Entferne gerade Nachbarn neben der ersten diagonalen Verbindung, damit
        # diese erhalten bleibt
        nächste.discard((romino[0][0], romino[1][1]))
        nächste.discard((romino[1][0], romino[0][1]))

    # Teste, ob dies das letze mal Generieren der Quadrate ist
    if len(romino) == größe - 1:
        # Finde alle Quadrate, für die y=0 gilt
        null = set(filter(lambda x: x[1] == 0, romino))

        # Teste, ob für keine Quadrate y=0 gilt
        if len(null) == 0:
            # Wenn für keine Quadrate y=0 gilt, muss im beim letzten mal
            # Generieren der Quadrate y=0 gelten
            # Filtere alle Quadrate raus, bei denen nicht y=0 gilt
            nächste = filter(lambda x: x[1] == 0, nächste)

    # Filtere alle Quadrate raus, die bereits im Romino vorhanden sind
    nächste = filter(lambda x: x not in romino, nächste)

    # Gib die generierten Quadrate zurück
    return nächste


def achsen_tauschen(romino):
    """Diese Funktion tauscht die x- und y-Achse eines Rominos"""
    return [x[::-1] for x in romino]


def spiegeln(romino, achse):
    """Diese Funktion spiegelt einen Romino auf einer Achse"""

    # Finde maximale Position auf der zu spiegelden Achse
    maximal = 0
    for quadrat in romino:
        if quadrat[achse] > maximal:
            maximal = quadrat[achse]

    # Spiegel den Romino
    if achse == 0:
        return [(maximal - x[0], x[1]) for x in romino]
    else:
        return [(x[0], maximal - x[1]) for x in romino]


def deckungsgleiche(romino):
    """Diese Funktion generiert alle Deckungsgleiche eines Romino"""

    # Liste für allen Deckunkgsgleichen
    deckungsgleiche = set()

    # Definiere alle nötigen Schritte zum generieren der Deckungsgleichen
    schritte = [
        (spiegeln, 0),
        (spiegeln, 1),
        (spiegeln, 0),
        (achsen_tauschen, ),
        (spiegeln, 0),
        (spiegeln, 1),
        (spiegeln, 0)
    ]

    # Gehe durch alle Schritte
    for schritt in schritte:
        # Führe Schritt aus
        romino = schritt[0](romino, *schritt[1:])

        # Sortiere Romino
        romino = tuple(sorted(romino))

        # Füge Romino hinzu
        deckungsgleiche.add(romino)

    # Gebe Deckungsgleiche zurück
    return deckungsgleiche


if __name__ == "__main__":
    # Teste ob alle Argumente angegeben wurden
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        # Wenn nicht alle Argumente angegeben wurden, zeige Informationen zu den
        # Argumenten
        print("Nutzung:", sys.argv[0], "n ausgabedatei")
        print("   oder:", sys.argv[0], "n")

        # Beende das Programm
        sys.exit()

    # Lese die Größe und evt. die Ausgabedatei ein
    größe = int(sys.argv[1])
    ab_halbe_größe = math.floor(größe / 2)
    auf_halbe_größe = math.ceil(größe / 2)
    datei = sys.argv[2] if len(sys.argv) == 3 else None

    print(f"Starte berechnung für n={größe}")

    # Generiere die ersten Quadrate des Rominos
    # Es werden zuerst nur die Quadrate an folgenden Positionen generiert:
    # Beispiel: Bei n=4
    #   +---> y
    #   |██░░
    #   |░░░░
    #   |░░░░
    # x V░░░░
    rominos = [[(0, y)] for y in range(ab_halbe_größe)]

    # Generiere alle weiteren Quadrate
    for _ in range(größe - 1):
        rominos = [x + [y] for x in rominos for y in nächste(x, größe, auf_halbe_größe)]

    # Bringe alle Quadrate der generierten Rominos in sortierte Reinfolge und
    # konvertiere zu einem Set
    rominos = {tuple(sorted(x)) for x in rominos}

    # Erstelle Set für die nach Deckungsgleichheit gefilterten Rominos
    gefilterte_rominos = set()

    # Erstelle Set für die deckungsgleichen Rominos der gefilterten Rominos
    deckungsgleiche_rominos = set()

    # Gehe durch alle Rominos
    for romino in rominos:
        # Teste ob Romino schon gefunden wurde
        if romino in deckungsgleiche_rominos:
            continue

        # Füge Romino und Deckungsgleiche des Rominos hinzu
        deckungsgleiche_rominos.update(deckungsgleiche(romino))
        gefilterte_rominos.add(romino)

    print(f"Es wurden {len(gefilterte_rominos)} Rominos gefunden.")

    # Teste ob eine Ausgabedatei angegeben wurde
    if datei is not None:
        # Speichere die Rominos ab

        # Entferne die Dateiendung
        datei = datei.split(".")
        datei = ".".join(datei[:-1]) if len(datei) > 1 else datei[0]

        print(f"Speichere Rominos in {datei}.txt ab.")

        # Öffne die Ausgabedatei zum schreiben
        datei = open(datei + ".txt", "w")

        # Schreibe die Anzahl und Größe der Rominos in die erste Zeile
        datei.write(
            f"{len(gefilterte_rominos)} Rominos der Größe n={größe}\n\n")

        # Iteriere durch alle gefilterten Rominos
        for romino in gefilterte_rominos:
            # Schreibe den Romino in die Ausgabedatei
            for x in range(größe):
                for y in range(größe):
                    if (x, y) in romino:
                        datei.write("█")
                    else:
                        datei.write("░")
                datei.write("\n")
            datei.write("\n")

        # Schließe die Ausgabedatei
        datei.close()
