import os
from helpers import root_path
os.chdir(root_path())

from Aufgaben import *
from skripte.erstellen import *

# Angaben für den Test im pdf-Dokument
schule = 'Torhorst - Gesamtschule'
schulart = 'mit gymnasialer Oberstufe'
Klasse = '11c'
Thema = 'Zehnerpotenzen'
datum_delta = 1  # in Tagen (0 ist Heute und 1 ist Morgen, 2 Übermorgen, usw.)
anzahl = 1 # wie viele verschiedenen Tests sollen erzeugt werden

for i in range(anzahl):
    # Hier die Aufgaben in der Form [[aufgabe1(), aufgabe2()],[aufgabe3(), aufgabe4()], usw.] eintragen
    Aufgaben = [[in_wiss_schreibweise_umf(1, anzahl=6), wiss_schreibweise_umf(2, anzahl=6),
                 einheiten_umrechnen(3, ['a'], anzahl=6),
                 einheiten_umrechnen(4, ['b'], anzahl=6)],
                 [einheiten_umrechnen(5, ['c'], anzahl=3),
                 einheiten_umrechnen(6, ['d'], anzahl=3)]]

    # hier werden aus der Liste der Aufgaben dieTest erzeugt
    liste_seiten = []
    for element in Aufgaben:
        liste_seiten.append(seite(element)) # z.b. liste_seiten = [seite(aufgaben_seite1), seite(aufgaben_seite2)]

    angaben = [schule, schulart, Klasse, Thema, datum_delta]
    arbeitsblatt_erzeugen(liste_seiten, angaben, i)
