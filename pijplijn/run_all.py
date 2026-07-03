"""Draai de volledige datapijplijn: haalt alle 7 datalagen op en schrijft ze naar data/*.geojson."""

import time

import afvalcontainers
import boulevards
import bruggen
import evenementen
import parkeergarages
import parkeerplaatsen
import winkelgevels

STAPPEN = [
    parkeerplaatsen,
    afvalcontainers,
    parkeergarages,
    winkelgevels,
    bruggen,
    boulevards,
    evenementen,
]


def main():
    for stap in STAPPEN:
        t0 = time.time()
        stap.main()
        print(f"  ({time.time() - t0:.1f}s)\n")


if __name__ == "__main__":
    main()
