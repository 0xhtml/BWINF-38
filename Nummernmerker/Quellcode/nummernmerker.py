#!/usr/bin/python3
import sys
import itertools
import math


def generiere_blöcke(nummer, block_ziffern):
    blöcke = []
    for block_ziffer in block_ziffern:
        blöcke.append(nummer[:block_ziffer])
        nummer = nummer[block_ziffer:]
    return blöcke


def generiere_mögliche_block_ziffern(nummer):
    maximale_block_anzahl = math.floor(len(nummer) / 2)
    minimale_block_anzahl = math.ceil(len(nummer) / 4)

    mögliche_block_ziffern = set()
    for block_anzahl in range(minimale_block_anzahl, maximale_block_anzahl + 1):
        block_ziffern = [[2, 3, 4] for _ in range(block_anzahl)]
        mögliche_block_ziffern.update(itertools.product(*block_ziffern))
    mögliche_block_ziffern = filter(lambda x: sum(
        x) == len(nummer), mögliche_block_ziffern)

    return mögliche_block_ziffern


def generiere_mögliche_blöcke(nummer, mögliche_block_ziffern):
    mögliche_blöcke = []
    for block_ziffern in mögliche_block_ziffern:
        mögliche_blöcke.append(generiere_blöcke(nummer, block_ziffern))

    return mögliche_blöcke


def zähle_nullen_am_anfang(blöcke):
    anzahl = 0
    for block in blöcke:
        if block[0] == "0":
            anzahl += 1
    return anzahl


def beste_blöcke(mögliche_blöcke):
    beste_nullen = math.inf
    beste_anzahl = math.inf
    beste_blöcke = None
    for blöcke in mögliche_blöcke:
        nullen = zähle_nullen_am_anfang(blöcke)
        if nullen < beste_nullen:
            beste_nullen = nullen
            beste_anzahl = len(blöcke)
            beste_blöcke = blöcke
        elif nullen == beste_nullen and len(blöcke) < beste_anzahl:
            beste_anzahl = len(blöcke)
            beste_blöcke = blöcke
    return beste_blöcke


if __name__ == "__main__":
    if len(sys.argv) != 2:
        # Es wurden nicht alle Argumente angegeben
        print("Benutzung:", sys.argv[0], "nummer")
        exit()

    mögliche_block_ziffern = generiere_mögliche_block_ziffern(sys.argv[1])
    mögliche_blöcke = generiere_mögliche_blöcke(sys.argv[1], mögliche_block_ziffern)
    beste_blöcke = beste_blöcke(mögliche_blöcke)

    print("\n".join(beste_blöcke))
