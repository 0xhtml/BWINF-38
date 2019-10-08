import sys
import itertools
import collections

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Benutzung:", sys.argv[0], "eingabedatei")
        exit()

    eingabe = open(sys.argv[1], "r").readlines()
    farbanzahl = int(eingabe[0])
    farben = ["blau", "gelb", "gruen", "orange", "rosa", "rot", "tuerkis"]
    bonus = [x.split()[:2] + [int(x.split()[2])] for x in eingabe[2:]]

    kombinationen = itertools.combinations(farben, farbanzahl)
    kombinationen = set(x + y for x in kombinationen for y in itertools.combinations_with_replacement(x, 9 - farbanzahl))
    kombinationen = set(y for x in kombinationen for y in itertools.permutations(x, 9))
    print(len(kombinationen))
