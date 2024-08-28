from Aufgaben import *
from skripte.erstellen import *

# Angaben für die Klausur im pdf-Dokument
Kurs = ('Grundkurs')
Klasse = 13
Gruppe = ''
Gesamtzeit = 285
Zeithmft = 90
datum_delta = 1  # in Tagen (0 ist Heute und 1 ist Morgen, 2 Übermorgen, usw.)
if Kurs != 'Grundkurs' and Kurs != 'Leistungskurs':
    exit("Kurs muss 'Grundkurs' oder 'Leistungskurs' sein.")

# Aufgaben für Teil I
liste_punkte_teil1 = ['Punkte']
liste_bez_teil1 = ['Aufgabe']

# Hier die Aufgaben in der Form [[aufgabe1(), aufgabe2()],[aufgabe3(), aufgabe4()], [ ..., aufgabe(10)]] eintragen
aufgaben_teil1 = [[ableitungen(1, ['a', 'b', 'c']), ableitungen(2, ['b']), ableitungen(3, ['c'])],
                  [ableitungen(4, ['d']), ableitungen(5, ['e']), ableitungen(6, ['f'])],
                  [ableitungen(7, ['a']), ableitungen(8, ['b']), ableitungen(9, ['c']),]]
                   # ableitungen(10, ['c'])]]

# hier werden aus der Liste der Aufgaben dieTest erzeugt
liste_seiten_teil1 = []
i = 0
for element in aufgaben_teil1:
    for aufgabe in element:
        liste_bez_teil1.append(str(i+1))
        liste_punkte_teil1.append(sum(aufgabe[-2]))
        i += 1
    liste_seiten_teil1.append(seite(element))

if Kurs == 'Grundkurs':
    exit('Es müssen 9 Aufgaben für den hilfsmittelfreien Teil ausgewählt werden.') if i != 9 else i
else:
    exit('Es müssen 10 Aufgaben für den hilfsmittelfreien Teil ausgewählt werden.') if i != 10 else i

# Hier die Aufgaben in der Form [[aufgabe1(), aufgabe2()],[aufgabe3(), aufgabe4()], usw.] eintragen
ana1 = [[kurvendiskussion_polynome_01(1)]]
ana2 = [[kurvendiskussion_exponentialfkt_01(2)]]
algebra = [[ebene_ebene(3,F_in_E='parallel')]]
stochastik = [[baumdiagramm(4)]]

aufgaben_teil2 = (ana1, ana2, algebra, stochastik)
liste_seiten_teil2 = []
liste_punkte_teil2 = []
liste_bez_teil2 = []
for aufgaben in aufgaben_teil2:
    liste_punkte = ['Punkte']
    liste_bez = ['Aufgabe']

    # hier werden aus der Liste der Aufgaben die Test erzeugt
    liste_seiten = []
    for element in aufgaben:
        for aufgabe in element:
            liste_bez.extend(aufgabe[5])
            liste_punkte.extend(aufgabe[4])
        liste_seiten.append(seite(element))
    liste_seiten_teil2.append(liste_seiten)
    liste_punkte_teil2.append(liste_punkte)
    liste_bez_teil2.append(liste_bez)

#  Angaben für die Klausur
angb_teil1 = [Kurs, datum_delta, liste_bez_teil1, liste_punkte_teil1]
angb_teil2 = [Kurs, datum_delta, liste_bez_teil2, liste_punkte_teil2]

vorabiturklausur(liste_seiten_teil1, angb_teil1, liste_seiten_teil2, angb_teil2)