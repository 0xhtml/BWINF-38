import sys


def mögliche_telepaartien(verteilung):
    """Finde alle möglichen Telepaartien"""

    # Erstelle Varaible für alle Möglichkeiten
    möglichkeiten = set()

    # Gehe durch alle Behälter kombinationen
    for behälter_a in range(len(verteilung)):
        for behälter_b in range(len(verteilung)):
            # Wenn Behälter A und B nicht der gleiche sind und die umgekehrte
            # Behälterkombination noch nicht gefunden wurde, füge die
            # Teleportation hinzu
            if behälter_a != behälter_b and (behälter_b, behälter_a) not in möglichkeiten:
                möglichkeiten.add((behälter_a, behälter_b))

    # Gebe die Telepaartiemöglichkeiten zurück
    return möglichkeiten


def telepaartiere(verteilung, behälter_a, behälter_b):
    """Führe eine Teleportation aus und gebe die neue Verteilung zurück"""

    # Wenn der erste Behälter weniger Biber als der Zweite enthält, tausche die
    # Reinfolge der Behälter für das Teleportieren
    if verteilung[behälter_a] < verteilung[behälter_b]:
        behälter_a, behälter_b = behälter_b, behälter_a

    # Ziehe von Behälter A die Biberanzahl von Behälter B ab
    verteilung[behälter_a] -= verteilung[behälter_b]

    # Verdopple die die Biberanzahl in Behälter B
    verteilung[behälter_b] *= 2

    # Gebe die neue Verteilung zurück
    return verteilung


def run(verteilung, tiefe):
    """Finde die LLL für eine Verteilung"""

    # Wenn die maximale Tiefe erreicht wurde, breche die Suche ab
    if tiefe == 0:
        return False

    # Finde alle möglichen Telepaartien
    telepaartien = mögliche_telepaartien(verteilung)

    # Erstelle Variable für die beste Möglichkeit
    bester = False

    # Gehe durch alle Telepaartien
    for telepaartie in telepaartien:
        # Füre die Telepartie aus und speichere die neue Verteilung
        telepaartierte_verteilung = telepaartiere(verteilung[:], *telepaartie)

        # Wenn in einem Behälter keine Biber mehr sind, ist die Teleportation
        # abgeschlossen. Gib also den Telepaartieschritt zurück
        if 0 in telepaartierte_verteilung:
            return [telepaartie]

        # Es müssen noch mehr Telepartie schritte geschehen, rufe diese Funktion
        # also rekursiv auf
        res = run(telepaartierte_verteilung, tiefe - 1)

        # Wenn ein Ergebnis gefunden wurde und dieses besser als das bisher
        # beste ergebnis ist, speichere das neue beste Ergebnis und setzte die
        # Tiefe herunter, damit nur noch nach kürzeren Möglichkeiten gesucht
        # wird
        if res != False and (bester == False or len(res) < len(bester)):
            bester = [telepaartie] + res
            tiefe = len(res)

    # Gebe die beste Möglichkeit zurück
    return bester


if __name__ == "__main__":
    # Teste ob alle Argumente angeben wurden
    if len(sys.argv) != 2 and len(sys.argv) != 4:
        # Wenn nicht alle Argumente angegeben wurden, zeige die Benutzung des
        # Programms
        print("Benutzung:", sys.argv[0], "n")
        print("      oder", sys.argv[0], "behälter1 behälter2 behälter3")

        # Beende das Programm
        sys.exit()

    # Teste welche Aktion durchgeführt werden soll.
    # A: Finde L(n), also die größte LLL für n Behälter
    # B: Finde die LLL für eine vorgegebene Verteilung
    if len(sys.argv) == 2:
        # Finde L(n)

        # Lese n ein
        n = int(sys.argv[1])

        # Finde alle möglichen Verteilungen
        verteilungen = []
        for a in range(1, n):
            for b in range(1, n - a):
                verteilungen.append([a, b, n - a - b])

        # Erstelle Variable für die kürzeste Folge von Telepartieschritten
        bester = []

        # Gehe durch alle Verteilungen
        for verteilung in verteilungen:
            # Finde die LLL mit einer maximalen Tiefe von n
            telepaartieschritte = run(verteilung, n)

            # Wenn die LLL kleiner ist wurde eine neue beste Möglichkeit
            # gefunden, speichere diese also als beste Möglichkeit ab
            if len(telepaartieschritte) > len(bester):
                bester = telepaartieschritte

        # Gebe L(n) zurück
        print(len(bester))
    else:
        # Finde LLL

        # Lese die Verteilung ein
        verteilung = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])]

        # Finde die LLL mit einer maximalen Tiefe von 50
        telepaartieschritte = run(verteilung, 50)

        # Gebe die Schritte aus
        for telepaartie in telepaartieschritte:
            # Speichere die vorhärige Verteilung
            a = str(verteilung)

            # Berechne die Verteilung nach der Telepartie
            verteilung = telepaartiere(verteilung, *telepaartie)
            c = str(verteilung)

            # Erstelle den Pfeil für die Ausgabe
            b = "  " + str(telepaartie[0] + 1) + " <"
            b += "-" * (len(a) - len(b) * 2)
            b += "> " + str(telepaartie[1] + 1)

            # Gebe den Teleportationsschritt aus
            print(a)
            print(b)
            print(c)
            print()

        # Gebe die Anzahl der Schritte aus
        print(len(telepaartieschritte), "Schritte")
