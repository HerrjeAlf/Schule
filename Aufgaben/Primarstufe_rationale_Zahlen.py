import string
import numpy as np
import random, math
from pylatex import (Document, NoEscape, SmallText, LargeText, MediumText, NewPage, Tabular, Alignat, Figure,
                     MultiColumn, MultiRow)
from pylatex.utils import bold
from random import *
from sympy import *
from sympy.plotting import plot
from skripte.funktionen import *
from skripte.plotten import *

a, b, c, d, e, f, g, h, x, y, z = symbols('a b c d e f g h x y z')
liste_teilaufg = list(string.ascii_lowercase)

def brueche_erweitern(nr, teilaufg=['a', 'b', 'c'], anzahl=False, anzahl_fakt=3, BE=[]):
    # Die SuS sollen Brüche mit vorgebenen Zahlen erweitern.
    # Mithilfe von "teilaufg=[]" können folgenden Funktionstypen (auch mehrfach der Form ['a', 'a', ...]) ausgewählt werden:
    # a) trivialer Bruch
    # b) einfacher Bruch
    # c) schwerer Bruch
    #
    # Mit 'anzahl=' kann eine Anzahl von zufällig ausgewählten Teilaufgaben aus den in 'teilaufg=[]' festgelegten Funktionstypen erstellt werden.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.
    # Der Parameter "anzahl_fakt=" gibt die Anzahl der Faktoren, mit denen die Brüche erweitert werden, vor.

    if anzahl != False:
        if type(anzahl) != int or anzahl > 27:
            exit("Der Parameter 'anzahl=' muss eine natürliche Zahl kleiner 27 sein.")
        teilaufg = [random.choice(teilaufg) for zahl in range(anzahl)]

    # Erstellen der Liste der Brüche mit Zähler und NenneR
    if teilaufg.count('a') > 9:
        print('Die maximale Anzahl an trivialen Brüchen ist 9.')
        trivial = 9
    else:
        trivial = teilaufg.count('a')
    liste_nenner = np.random.choice(list(range(2,12)), trivial, False)
    liste_nenner.sort()
    liste_brueche = [[1,element] for element in liste_nenner]

    if teilaufg.count('b') > 9:
        print('Die maximale Anzahl an einfachen Brüchen ist 9.')
        einfach = 9
    else:
        einfach = teilaufg.count('b')
    for zahl in range(einfach):
        zaehler, nenner = np.random.choice([2, 3, 5, 7], 2, False)
        while [zaehler, nenner] in liste_brueche:
            zaehler, nenner = np.random.choice([2, 3, 5, 7], 2, False)
        liste_brueche.append([zaehler, nenner])

    if teilaufg.count('c') > 9:
        print('Die maximale Anzahl an schwierigen Brüchen ist 9.')
        schwer = 9
    else:
        schwer = teilaufg.count('c')
    for zahl in range(schwer):
        zaehler, nenner = np.random.choice([5, 7, 11, 13], 2, False)
        while [zaehler, nenner] in liste_brueche:
            zaehler, nenner = np.random.choice([5, 7, 11, 13], 2, False)
        liste_brueche.append([zaehler, nenner])

    # Erstellen der Faktorliste
    anzahl_fakt = 6 if anzahl_fakt > 6 else anzahl_fakt
    liste_faktoren = np.random.choice([2, 3, 5, 7, 11, 13], anzahl_fakt, False)
    liste_faktoren.sort()

    # Erstellen der Aufgabenstellung
    aufg_faktoren = ''
    for faktor in liste_faktoren:
        if faktor != liste_faktoren[-1]:
            aufg_faktoren = aufg_faktoren + gzahl(faktor) + ', '
        else:
            aufg_faktoren = aufg_faktoren + gzahl(faktor)

    liste_bez = [f'{str(nr)}']
    i = 0
    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               f'Erweitern Sie die gegebenen Brüche mit {aufg_faktoren}.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []

    aufg = ''
    lsg = ''
    punkte = 0
    for element in liste_brueche:
        zaehler, nenner = element[0], element[1]
        if (i + 1) % 6 != 0:
            aufg = aufg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner) + '~}'
            if i + 1 < trivial + einfach + schwer:
                aufg = aufg + r' \hspace{5em} '
        elif (i + 1) % 6 == 0 and element != liste_brueche[-1]:
            aufg = (aufg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner)
                    + r'~} \\\\')
        else:
            aufg = aufg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner) + '~}'
        liste_brueche_lsg = [[zaehler*faktor, nenner*faktor] for faktor in liste_faktoren]
        lsg_teilaufg = ''
        for tubel in liste_brueche_lsg:
            if tubel != liste_brueche_lsg[-1]:
                lsg_teilaufg = lsg_teilaufg + r' \frac{' + gzahl(tubel[0]) + '}{' + gzahl(tubel[1]) + '} ~=~ '
            else:
                lsg_teilaufg = lsg_teilaufg + r' \frac{' + gzahl(tubel[0]) + '}{' + gzahl(tubel[1]) + r'}'
        if (i + 1) % 2 != 0 and i + 1 != trivial + einfach + schwer:
            lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{' + gzahl(zaehler) + '}{' + gzahl(nenner) + '} ~=~ '
                   + lsg_teilaufg + r' \hspace{5em}')
        else:
            lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{' + gzahl(zaehler) + '}{' + gzahl(nenner) + '} ~=~ '
                   + lsg_teilaufg + r' \\\\')
        punkte += 1
        i += 1
    lsg = lsg + r' \\ \mathrm{insgesamt~' + str(punkte) + r'~Punkte}'
    if BE != []:
        if len(BE) > 1:
            print(
                'Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. '
                'Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]
a, b, c, d, e, f, g, h, x, y, z
def brueche_kuerzen(nr, teilaufg=['a', 'b', 'c'], anzahl=False, BE=[]):
    # Die SuS sollen Brüche mit so weit wie möglich kürzen.
    # Mithilfe von "teilaufg=[]" können folgenden Funktionstypen (auch mehrfach der Form ['a', 'a', ...]) ausgewählt werden:
    # a) trivialer Bruch
    # b) einfacher Bruch
    # c) schwerer Bruch
    #
    # Mit 'anzahl=' kann eine Anzahl von zufällig ausgewählten Teilaufgaben aus den in 'teilaufg=[]' festgelegten Funktionstypen erstellt werden.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.
    # Der Parameter "anzahl_fakt=" gibt die Anzahl der Faktoren, mit denen die Brüche erweitert werden, vor.

    liste_bez = [f'{str(nr)}']
    i = 0
    aufg = ''
    lsg = ''
    punkte = 0

    if anzahl != False:
        if type(anzahl) != int or anzahl > 27:
            exit("Der Parameter 'anzahl=' muss eine natürliche Zahl kleiner 27 sein.")
        teilaufg = [random.choice(teilaufg) for zahl in range(anzahl)]

    # Erstellen der Liste der Brüche mit Zähler und NenneR
    if teilaufg.count('a') > 9:
        print('Die maximale Anzahl an trivialen Brüchen ist 9.')
        trivial = 9
    else:
        trivial = teilaufg.count('a')
    liste_nenner = np.random.choice(list(range(2,12)), trivial, False)
    liste_nenner.sort()
    liste_brueche_aufg = []
    for zahl in liste_nenner:
        faktor = random.choice([2, 3, 5, 7, 10])
        liste_brueche_aufg.append([faktor, faktor*zahl])
        lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(faktor) + '~}{~' + gzahl(faktor * zahl)
               + r'~} ~=~ \frac{ ~' + gzahl(1) + '~}{~' + gzahl(zahl) + r'~}')
        if (i + 1) % 3 != 0 and i + 1 < len(teilaufg):
            lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 3 == 0 or i + 1 == trivial and i + 1 < len(teilaufg):
            lsg = lsg + r' \\\\'
        else:
            pass
        i += 1
        punkte += 1
    if teilaufg.count('b') > 9:
        print('Die maximale Anzahl an einfachen Brüchen ist 9.')
        einfach = 9
    else:
        einfach = teilaufg.count('b')

    for zahl in range(einfach):
        fkt = np.random.choice([2, 3, 4, 5, 6, 7, 10], 2, False)
        fkt.sort()
        zaehler, nenner = np.random.choice([2, 3, 5, 7, 11], 2, False)
        while [zaehler, nenner] in liste_brueche_aufg:
            zaehler, nenner = np.random.choice([2, 3, 5, 7, 11], 2, False)
        liste_brueche_aufg.append([zaehler*fkt[0]*fkt[1], nenner*fkt[0]*fkt[1]])
        lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler * fkt[0] * fkt[1]) + '~}{~'
               + gzahl(nenner * fkt[0] * fkt[1]) + r'~} ~=~ \frac{ ~' + gzahl(zaehler * fkt[0]) + '~}{~'
               + gzahl(nenner * fkt[0]) + r'~} ~=~ \frac{ ~' + gzahl(zaehler) + '~}{~' + gzahl(nenner) + r'~}')
        if (i + 1) % 3 != 0 and i + 1 < len(teilaufg):
            lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 3 == 0 or i + 1 == einfach and i + 1 < len(teilaufg):
            lsg = lsg + r' \\\\'
        else:
            pass
        i += 1
        punkte += 1

    if teilaufg.count('c') > 9:
        print('Die maximale Anzahl an schwierigen Brüchen ist 9.')
        schwer = 9
    else:
        schwer = teilaufg.count('c')
    for zahl in range(schwer):
        fkt = np.random.choice([2, 3, 4, 5, 6, 7, 10], 3, False)
        fkt.sort()
        zaehler, nenner = np.random.choice([3, 5, 7, 11, 13], 2, False)
        while [zaehler, nenner] in liste_brueche_aufg:
            zaehler, nenner = np.random.choice([3, 5, 7, 11, 13], 2, False)
        liste_brueche_aufg.append([zaehler*fkt[0]*fkt[1]*fkt[2], nenner*fkt[0]*fkt[1]*fkt[2]])
        lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler * fkt[0] * fkt[1] * fkt[2]) + '~}{~'
               + gzahl(nenner * fkt[0] * fkt[1] * fkt[2]) + r'~} ~=~ \frac{ ~' + gzahl(
                    zaehler * fkt[0] * fkt[1]) + '~}{~'
               + gzahl(nenner * fkt[0] * fkt[1]) + r'~} ~=~ \frac{ ~' + gzahl(zaehler * fkt[0]) + '~}{~'
               + gzahl(nenner * fkt[0]) + r'~} ~=~ \frac{ ~' + gzahl(zaehler) + '~}{~' + gzahl(nenner) + r'~}')
        if (i + 1) % 2 != 0 and i + 1 < len(teilaufg):
                lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 2 == 0 or i + 1 == einfach and i + 1 < len(teilaufg):
            lsg = lsg + r' \\\\'
        else:
            pass
        i += 1
        punkte += 1

    # Erstellen der Aufgabenstellung
    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               f'Kürzen Sie die gegebenen Brüche soweit wie möglich.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []
    k = 0

    for element in liste_brueche_aufg:
        zaehler, nenner = element[0], element[1]
        if (k + 1) % 5 != 0:
            aufg = aufg + str(liste_teilaufg[k]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner) + '~}'
            if k + 1 < trivial + einfach + schwer:
                aufg = aufg + r' \hspace{5em} '
        elif (k + 1) % 5 == 0 and (k + 1) < trivial + einfach + schwer:
            aufg = (aufg + str(liste_teilaufg[k]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner)
                    + r'~} \\\\')
        else:
            aufg = aufg + str(liste_teilaufg[k]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner) + '~}'
        k += 1

    lsg = lsg + r' \\\\ \mathrm{insgesamt~' + str(punkte) + r'~Punkte}'
    if BE != []:
        if len(BE) > 1:
            print(
                'Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. '
                'Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]

def brueche_ergaenzen(nr, teilaufg=['a', 'b'], anzahl=False, BE=[]):
    # Die SuS sollen eine vorgegebene Gleichung von Bruchtermen so ergänzen, dass diese richtig ist.
    # Mithilfe von "teilaufg=[]" können folgenden Funktionstypen (auch mehrfach der Form ['a', 'a', ...]) ausgewählt werden:
    # a) Gleichung von Bruchtermen mit unbekannten Nenner
    # b) Gleichung von Bruchtermen mit unbekannten Zähler
    #
    # Mit 'anzahl=' kann eine Anzahl von zufällig ausgewählten Teilaufgaben aus den in 'teilaufg=[]' festgelegten Funktionstypen erstellt werden.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.
    # Der Parameter "anzahl_fakt=" gibt die Anzahl der Faktoren, mit denen die Brüche erweitert werden, vor.

    liste_bez = [f'{str(nr)}']
    i = 0
    punkte = 0

    if anzahl != False:
        if type(anzahl) != int or anzahl > 13:
            exit("Der Parameter 'anzahl=' muss eine natürliche Zahl kleiner 13 sein.")
        teilaufg = [random.choice(teilaufg) for zahl in range(anzahl)]

    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               f'Ergänzen Sie die Terme so, dass die jeweilige Gleichung stimmt.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []
    liste_brueche = []
    aufg = ''
    lsg = ''
    unbek_nenner = teilaufg.count('a')
    for zahl in range(unbek_nenner):
        fakt = random.choice([2, 3, 4, 5, 6, 7, 10])
        zaehler, nenner = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 2, False)
        while [zaehler, nenner] in liste_brueche:
            zaehler, nenner = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 2, False)
        liste_brueche.append([zaehler, nenner])
        aufg = (aufg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner)
               + r'~} ~=~ \frac{~' + gzahl(zaehler * fakt) + r'~}{ \quad }')
        lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner)
               + r'~} ~=~ \frac{~' + gzahl(zaehler * fakt) + r'~}{~ \mathbf{' + gzahl(nenner * fakt) + '}~}')
        if (i + 1) % 3 != 0 and i + 1 < nenner + zaehler:
                aufg = aufg + r' \hspace{5em} '
                lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 3 == 0 and (i + 1) < len(teilaufg):
            aufg = aufg + r' \\\\'
            lsg = lsg + r' \\\\'
        else:
            pass
        punkte += 1
        i += 1
    unbek_zaehler = teilaufg.count('b')
    for zahl in range(unbek_zaehler):
        fakt = random.choice([2, 3, 4, 5, 6, 7, 10])
        zaehler, nenner = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 2, False)
        while [zaehler, nenner] in liste_brueche:
            zaehler, nenner = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 2, False)
        liste_brueche.append([zaehler, nenner])
        aufg = (aufg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner)
                + r'~} ~=~ \frac{ \quad }{~' + gzahl(nenner * fakt) + r'~}')
        lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{~' + gzahl(zaehler) + '~}{~' + gzahl(nenner)
               + r'~} ~=~ \frac{~ \mathbf{' + gzahl(zaehler * fakt) + r'} ~}{~' + gzahl(nenner * fakt) + '~}')
        if (i + 1) % 3 != 0 and i + 1 < nenner + zaehler:
                aufg = aufg + r' \hspace{5em} '
                lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 3 == 0 and (i + 1) < len(teilaufg):
            aufg = aufg + r' \\\\'
            lsg = lsg + r' \\\\'
        else:
            pass
        punkte += 1
        i += 1
    lsg = lsg + r' \\\\ \mathrm{insgesamt~' + str(punkte) + r'~Punkte}'
    if BE != []:
        if len(BE) > 1:
            print('Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. '
                'Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]

def bruchteile_berechnen(nr, anzahl=2, BE=[]):
    # Die SuS sollen von einer gegebenen Menge den angegebenen Bruchteil berechnen.
    # Der Parameter "anzahl=" legt die Anzahl der Teilaufgaben fest. Sie kann maximal 12 betragen.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.

    liste_bez = [f'{str(nr)}']
    i = 0
    punkte = 0

    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               f'Berechne.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []
    anzahl = 12 if anzahl > 12 else anzahl

    aufg = ''
    lsg = ''
    for zahl in range(anzahl):
        bruch = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2, False)
        bruch.sort()
        zaehler, nenner = bruch
        einheiten = random.choice(['min', 'l', 'kg', 'g', 'qm', 'km'])
        zahl = random.randint(20, 100)
        wert = zaehler * zahl
        punkte += 1
        aufg = (aufg + str(liste_teilaufg[i]) + r') \quad  \frac{' + gzahl(zaehler) + '}{' + gzahl(nenner)
                + r'} ~ \mathrm{von} ~ ' + gzahl(zahl * nenner) + einheiten)
        lsg = (lsg + str(liste_teilaufg[i]) + r') \quad \frac{' + gzahl(zaehler) + '}{' + gzahl(nenner) + r'} \cdot '
               + gzahl(zahl * nenner) + einheiten + '~=~' + gzahl(wert) + einheiten)
        if (i + 1) % 3 != 0 and i + 1 < anzahl:
            aufg = aufg + r' \hspace{5em} '
            lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 3 == 0 and i + 1 < anzahl:
            aufg = aufg + r' \\\\'
            lsg = lsg + r' \\\\'
        i += 1

    lsg = lsg + r' \\\\ \mathrm{insgesamt~' + str(punkte) + r'~Punkte}'
    if BE != []:
        if len(BE) > 1:
            print(
                'Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. '
                'Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]

def brueche_add_subr(nr, teilaufg=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], anzahl=False, BE=[]):
    # Hier sollen die SuS gleichnamige und ungleichnamige Brüche addieren und subtrahieren.
    # Mithilfe von "teilaufg=[]" können folgende Bruchterme (auch mehrfach z.B. der Form ['a', 'a', ...]) ausgewählt werden:
    # a) einfacher gleichnamiger Bruchterm (beide positiv)
    # b) gleichnamiger Bruchterm (beide positiv)
    # c) gleichnamiger Bruchterm (zweiter negativ)
    # d) gleichnamiger Bruchterm (beide negativ)
    # e) beliebiger gleichnamiger Bruch
    # f) einfacher ungleichnamiger Bruchterme (beide positiv)
    # g) ungleichnamiger Bruchterm (beide positiv)
    # h) ungleichnamiger Bruchterm (zweiter negativ)
    # i) ungleichnamiger Bruchterm (beide negativ)
    # j) beliebiger ungleichnamiger Bruchterm
    #
    # Mit 'anzahl=' kann eine Anzahl von zufällig ausgewählten Teilaufgaben aus den in 'teilaufg=[]' festgelegten Arten Bruchtermen erstellt werden.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.

    liste_bez = [f'{str(nr)}']
    i = 0

    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               'Berechne den angegebenen Bruchterm.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []

    def einf_pp_gleichn_bruchterm():
        zaehler_2, zaehler_1 = np.random.choice([1, 2, 3, 4, 5, 6], 2, False)
        nenner = zaehler_1 + zaehler_2 + nzahl(2,4)
        loesung = Rational(zaehler_1 + zaehler_2, nenner)
        aufg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner) + r'} ~+~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner) + r'}')
        lsg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner) + r'} ~+~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner) + r'} ~=~ \frac{' + gzahl(zaehler_1) + '+' + gzahl(zaehler_2) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def pp_gleichn_bruchterm():
        zaehler_2, zaehler_1, nenner = np.random.choice(range(2,12), 3, False)
        loesung = Rational(zaehler_1 + zaehler_2, nenner)
        aufg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner) + r'} ~+~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner) + r'}')
        lsg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner) + r'} ~+~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner) + r'} ~=~ \frac{' + gzahl(zaehler_1) + '~+~' + gzahl(zaehler_2) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def pn_gleichn_bruchterm():
        zaehler_2, zaehler_1, nenner = np.random.choice(range(2,12), 3, False)
        loesung = Rational(zaehler_1 - zaehler_2, nenner)
        aufg = (r' \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner) + r'} ~-~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner) + r'}')
        lsg = (r' \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner) + r'} ~-~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner) + r'} ~=~ \frac{' + gzahl(zaehler_1) + '~-~' + gzahl(zaehler_2) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def nn_gleichn_bruchterm():
        zaehler_2, zaehler_1, nenner = np.random.choice(range(2,12), 3, False)
        loesung = Rational(-1*(zaehler_1 + zaehler_2), nenner)
        aufg = (r' - \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner) + r'} ~-~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner) + r'}')
        lsg = (r' - \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner) + r'} ~-~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner) + r'} ~=~ \frac{ - ' + gzahl(zaehler_1) + '~-~' + gzahl(zaehler_2) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def bel_gleichn_bruchterm():
        zaehler_1, zaehler_2, nenner = np.random.choice(range(2,12), 3, False)
        vorz1, vorz2 = np.random.choice([1, -1], 2, True)
        loesung = Rational(vorz1*zaehler_1 + vorz2*zaehler_2, nenner)
        aufg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner) + r'} ~' + vorz(vorz2) + r'~ \frac{'
                + gzahl(zaehler_2) + '}{' + gzahl(nenner) + r'}')
        lsg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner) + r'} ~' + vorz(vorz2)
               + r'~ \frac{' + gzahl(zaehler_2) + '}{' + gzahl(nenner) + r'} ~=~ \frac{' + gzahl(vorz1*zaehler_1)
               + vorz_str(vorz2*zaehler_2) + '}{' + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def einf_pp_ungl_bruchterm():
        zaehler_1, zaehler_2, nenner_1, nenner_2 = np.random.choice(range(2,10), 4, False)
        nenner = kgv(nenner_1, nenner_2)
        zaehler_1_erw = nenner / nenner_1 * zaehler_1
        zaehler_2_erw = nenner / nenner_2 * zaehler_2
        loesung = Rational(zaehler_1_erw + zaehler_2_erw, nenner)
        aufg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~+~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner_2) + r'}')
        lsg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~+~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner_2) + r'} ~=~ \frac{' + gzahl(zaehler_1_erw) + '+' + gzahl(zaehler_2_erw) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def pp_ungl_bruchterm():
        zaehler_1, zaehler_2, nenner_1, nenner_2 = np.random.choice(range(2,12), 4, False)
        nenner = kgv(nenner_1, nenner_2)
        zaehler_1_erw = nenner / nenner_1 * zaehler_1
        zaehler_2_erw = nenner / nenner_2 * zaehler_2
        loesung = Rational(zaehler_1_erw + zaehler_2_erw, nenner)
        aufg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~+~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner_2) + r'}')
        lsg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~+~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner_2) + r'} ~=~ \frac{' + gzahl(zaehler_1_erw) + '+' + gzahl(zaehler_2_erw) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def pn_ungl_bruchterm():
        zaehler_1, zaehler_2, nenner_1, nenner_2 = np.random.choice(range(2,12), 4, False)
        nenner = kgv(nenner_1, nenner_2)
        zaehler_1_erw = nenner / nenner_1 * zaehler_1
        zaehler_2_erw = nenner / nenner_2 * zaehler_2
        loesung = Rational(zaehler_1_erw - zaehler_2_erw, nenner)
        aufg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~-~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner_2) + r'}')
        lsg = (r' \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~-~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner_2) + r'} ~=~ \frac{' + gzahl(zaehler_1_erw) + '-' + gzahl(zaehler_2_erw) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def nn_ungl_bruchterm():
        zaehler_1, zaehler_2, nenner_1, nenner_2 = np.random.choice(range(2,12), 4, False)
        nenner = kgv(nenner_1, nenner_2)
        zaehler_1_erw = nenner / nenner_1 * zaehler_1
        zaehler_2_erw = nenner / nenner_2 * zaehler_2
        loesung = Rational(-1*(zaehler_1_erw + zaehler_2_erw), nenner)
        aufg = (r' - \frac{' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~-~ \frac{' + gzahl(zaehler_2)
                + '}{' + gzahl(nenner_2) + r'}')
        lsg = (r' - \frac{ ' + gzahl(zaehler_1) +'}{' + gzahl(nenner_1) + r'} ~-~ \frac{' + gzahl(zaehler_2)
               + '}{' + gzahl(nenner_2) + r'} ~=~ \frac{ - ' + gzahl(zaehler_1_erw) + '-' + gzahl(zaehler_2_erw) + '}{'
               + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    def bel_ungl_bruchterm():
        zaehler_1, zaehler_2, nenner_1, nenner_2 = np.random.choice(range(2,12), 4, False)
        vorz1, vorz2 = np.random.choice([1, -1], 2, True)
        nenner = kgv(nenner_1, nenner_2)
        zaehler_1_erw = vorz1 * nenner / nenner_1 * zaehler_1
        zaehler_2_erw = vorz2 * nenner / nenner_2 * zaehler_2
        loesung = Rational(zaehler_1_erw + zaehler_2_erw, nenner)
        aufg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner_1) + r'} ~' + vorz(vorz2)
                + r'~ \frac{' + gzahl(zaehler_2) + '}{' + gzahl(nenner_2) + r'}')
        lsg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(zaehler_1) + '}{' + gzahl(nenner_1) + r'} ~' + vorz(vorz2)
                + r'~ \frac{' + gzahl(zaehler_2) + '}{' + gzahl(nenner_2) + r'} ~=~ \frac{' + gzahl(zaehler_1_erw)
               + vorz_str(zaehler_2_erw) + '}{' + gzahl(nenner) + r'} ~=~ ' + gzahl(loesung))
        return aufg, lsg

    if anzahl != False:
        if type(anzahl) != int or anzahl > 26:
            exit("Der Parameter 'anzahl=' muss eine natürliche Zahl kleiner 27 sein.")
        teilaufg = np.random.choice(teilaufg, anzahl, True)
    aufgaben = {'a': einf_pp_gleichn_bruchterm, 'b': pp_gleichn_bruchterm, 'c': pn_gleichn_bruchterm,
                'd': nn_gleichn_bruchterm, 'e': bel_gleichn_bruchterm, 'f': einf_pp_ungl_bruchterm,
                'g': pp_ungl_bruchterm, 'h': pn_ungl_bruchterm, 'i': nn_ungl_bruchterm, 'j':bel_ungl_bruchterm}

    aufg = ''
    lsg = ''
    punkte = 0
    for element in teilaufg:
        teilaufg_aufg, teilaufg_lsg = aufgaben[element]()
        aufg = aufg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_aufg
        lsg = lsg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_lsg
        if (i+1) % 4 != 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \hspace{5em} '
        elif (i + 1) % 4 == 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \\\\'
        if (i+1) % 2 != 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 2 == 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \\\\'
        else:
            pass
        punkte += 1
        i += 1

    lsg = lsg + r' \\\\ \mathrm{insgesamt~' + str(punkte) + r'~Punkte}'
    if BE != []:
        if len(BE) > 1:
            print('Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]

def brueche_mul_div(nr, teilaufg=['a', 'b', 'c', 'd', 'e', 'f'], anzahl=False, BE=[]):
    # Hier sollen die SuS Brüche multiplizieren und dividieren.
    # Mithilfe von "teilaufg=[]" können folgende Bruchterme (auch mehrfach z.B. der Form ['a', 'a', ...]) ausgewählt werden:
    # a) einfachen Bruchterm multiplizieren (beide positiv)
    # b) einfachen Bruchterm multiplizieren (beliebige Vorzeichen)
    # c) Bruchterm kürzen und multiplizieren (beliebige Vorzeichen)
    # a) einfachen Bruchterm dividieren (beide positiv)
    # b) einfachen Bruchterm dividieren (beliebige Vorzeichen)
    # c) Bruchterm kürzen und dividieren (beliebige Vorzeichen)
    #
    # Mit 'anzahl=' kann eine Anzahl von zufällig ausgewählten Teilaufgaben aus den in 'teilaufg=[]' festgelegten Arten Bruchtermen erstellt werden.

    liste_bez = [f'{str(nr)}']
    i = 0
    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               'Berechne den engegebenen Bruchterm.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []

    def einf_pp_bruchterm_multi():
        zahlen = np.random.choice(range(1,10), 4, False)
        zahlen.sort()
        zaehler1, zaehler2, nenner1, nenner2 = zahlen
        bruch1 = Rational(zaehler1, nenner1)
        bruch2 = Rational(zaehler2, nenner2)
        ergebnis = Rational(zaehler1 * zaehler2, nenner1 * nenner2)
        aufg = gzahl(bruch1) + r'~ \cdot ~' + gzahl(bruch2)
        lsg = gzahl(bruch1) + r'~ \cdot ~' + gzahl(bruch2) + '~=~' + gzahl(ergebnis)
        return aufg, lsg

    def einf_bruchterm_multi():
        zahlen = np.random.choice(range(1,10), 4, False)
        zahlen.sort()
        zaehler1, zaehler2, nenner1, nenner2 = zahlen
        vorz1, vorz2 = np.random.choice([1, -1], 2, True)
        bruch1 = Rational(vorz1 * zaehler1, nenner1)
        bruch2 = Rational(vorz2 * zaehler2, nenner2)
        ergebnis = Rational(vorz1 * vorz2 * zaehler1 * zaehler2, nenner1 * nenner2)
        aufg = gzahl(bruch1) + r'~ \cdot ~' + gzahl_klammer(bruch2)
        lsg = gzahl(bruch1) + r'~ \cdot ~' + gzahl_klammer(bruch2) + '~=~' + gzahl(ergebnis)
        return aufg, lsg

    def bruchterm_kuerz_multi():
        zahlen = np.random.choice(range(1,12), 4, False)
        zahlen.sort()
        zaehler1, zaehler2, nenner1, nenner2 = zahlen
        while (nenner1/zaehler1) % 1 == 0 or (nenner2/zaehler2) % 1 == 0:
            zahlen = np.random.choice(range(1, 12), 4, False)
            zahlen.sort()
            zaehler1, zaehler2, nenner1, nenner2 = zahlen
        vorz1, vorz2 = np.random.choice([1, -1], 2, True)
        fakt1, fakt2 = np.random.choice(range(2,12), 2, False)
        ergebnis = Rational(vorz1 * vorz2 * zaehler1 * zaehler2, nenner1 * nenner2)
        if vorz2 < 0:
            aufg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2*zaehler1) + '}{' + gzahl(fakt1*nenner1)
                    + r'}~ \cdot ~ \left(' + vorz_aussen(vorz2) + r' \frac{' + gzahl(fakt1 * zaehler2) + '}{'
                    + gzahl(fakt2 * nenner2) + r'} \right)')
            lsg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1)
                   + r'} ~ \cdot ~ \left( ' + vorz_aussen(vorz2) + r' \frac{' + gzahl(fakt1 * zaehler2) + '}{'
                   + gzahl(fakt2 * nenner2) + r'} \right) ~=~' + vorz_aussen(vorz1*vorz2) + r' \frac{'
                   + gzahl(zaehler1) + '}{' + gzahl(nenner1) + r'} \cdot \frac{' + gzahl(zaehler2) + '}{'
                   + gzahl(nenner2) + r'} ~=~' + gzahl(ergebnis))
        else:
            aufg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1)
                    + r'} ~ \cdot ~' + vorz_aussen(vorz2) + r' \frac{' + gzahl(fakt1 * zaehler2) + '}{'
                    + gzahl(fakt2 * nenner2) + r'}')
            lsg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1)
                   + r'} ~ \cdot ~' + vorz_aussen(vorz2) + r' \frac{' + gzahl(fakt1 * zaehler2) + '}{'
                   + gzahl(fakt2 * nenner2) + r'} ~=~' + vorz_aussen(vorz1 * vorz2) + r' \frac{'
                   + gzahl(zaehler1) + '}{' + gzahl(nenner1) + r'} \cdot \frac{'
                   + gzahl(zaehler2) + '}{' + gzahl(nenner2) + r'} ~=~' + gzahl(ergebnis))
        return aufg, lsg
    def einf_pp_bruchterm_div():
        zahlen = np.random.choice(range(1, 10), 4, False)
        zahlen.sort()
        zaehler1, zaehler2, nenner1, nenner2 = zahlen
        bruch1 = Rational(zaehler1, nenner1)
        bruch2 = Rational(zaehler2, nenner2)
        bruch2_kw = Rational(nenner2, zaehler2)
        ergebnis = Rational(zaehler1 * nenner2, nenner1 * zaehler2)
        aufg = gzahl(bruch1) + r'~ \div ~' + gzahl(bruch2)
        lsg = (gzahl(bruch1) + r' \div ' + gzahl(bruch2) + '~=~' + gzahl(bruch1) + r' \cdot '
               + gzahl(bruch2_kw) + '~=~' + gzahl(ergebnis))
        return aufg, lsg

    def einf_bruchterm_div():
        zahlen = np.random.choice(range(1,10), 4, False)
        zahlen.sort()
        zaehler1, zaehler2, nenner1, nenner2 = zahlen
        vorz1, vorz2 = np.random.choice([1, -1], 2, True)
        bruch1 = Rational(zaehler1, nenner1)
        bruch2 = Rational(zaehler2, nenner2)
        bruch2_kw = Rational(nenner2, zaehler2)
        ergebnis = Rational(vorz1 * vorz2 * zaehler1 * nenner2, nenner1 * zaehler2)
        aufg = gzahl(vorz1 * bruch1) + r'~ \div ~' + gzahl_klammer(vorz2 * bruch2)
        lsg = (gzahl(vorz1 * bruch1) + r' \div ' + gzahl_klammer(vorz2*bruch2) + '~=~' + vorz_aussen(vorz1*vorz2)
               + gzahl(bruch1) + r' \cdot ' + gzahl(bruch2_kw) + '~=~' + gzahl(ergebnis))
        return aufg, lsg

    def bruchterm_kuerz_div():
        zahlen = np.random.choice(range(1, 12), 4, False)
        zahlen.sort()
        zaehler1, zaehler2, nenner1, nenner2 = zahlen
        while (nenner1 / zaehler1) % 1 == 0 or (nenner2 / zaehler2) % 1 == 0:
            zahlen = np.random.choice(range(1, 12), 4, False)
            zahlen.sort()
            zaehler1, zaehler2, nenner1, nenner2 = zahlen
        vorz1, vorz2 = np.random.choice([1, -1], 2, True)
        fakt1, fakt2 = np.random.choice(range(2, 12), 2, False)
        ergebnis = Rational(vorz1 * vorz2 * zaehler1 * nenner2, nenner1 * zaehler2)
        if vorz2 < 0:
            aufg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1)
                    + r'} ~ \div ~ \left(' + vorz_aussen(vorz2) + r' \frac{' + gzahl(fakt2 * zaehler2) + '}{'
                    + gzahl(fakt1 * nenner2) + r'} \right)')
            lsg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1)
                   + r'} ~ \div \left(' + vorz_aussen(vorz2) + r'~ \frac{' + gzahl(fakt2 * zaehler2) + '}{'
                   + gzahl(fakt1 * nenner2) + r'} \right) ~=~' + vorz_aussen(vorz1 * vorz2) + r' \frac{'
                   + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1) + r'} \cdot \frac{'
                   + gzahl(fakt1 * nenner2) + '}{' + gzahl(fakt2 * zaehler2) + r'} ~=~'
                   + vorz_aussen(vorz1 * vorz2) + r' \frac{' + gzahl(zaehler1) + '}{' + gzahl(nenner1)
                   + r'} \cdot \frac{' + gzahl(nenner2) + '}{' + gzahl(zaehler2) + r'} ~=~' + gzahl(ergebnis))
        else:
            aufg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1)
                    + r'}~ \div ~' + vorz_aussen(vorz2) + r' \frac{' + gzahl(fakt2 * zaehler2) + '}{'
                    + gzahl(fakt1 * nenner2) + r'} ')
            lsg = (vorz_aussen(vorz1) + r' \frac{' + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1)
                   + r'} ~ \div ' + vorz_aussen(vorz2) + r'~ \frac{' + gzahl(fakt2 * zaehler2) + '}{'
                   + gzahl(fakt1 * nenner2) + r'} ~=~' + vorz_aussen(vorz1) + r' \frac{'
                   + gzahl(fakt2 * zaehler1) + '}{' + gzahl(fakt1 * nenner1) + r'} ~ \cdot \frac{'
                   + gzahl(fakt1 * nenner2) + '}{' + gzahl(fakt2 * zaehler2) + r'} ~=~' + vorz_aussen(vorz1)
                   + r' \frac{' + gzahl(zaehler1) + '}{' + gzahl(nenner1) + r'} \cdot \frac{' + gzahl(nenner2)
                   + '}{' + gzahl(zaehler2)+ r'} ~=~' + gzahl(ergebnis))
        return aufg, lsg


    if anzahl != False:
        if type(anzahl) != int or anzahl > 26:
            exit("Der Parameter 'anzahl=' muss eine natürliche Zahl kleiner 27 sein.")
        teilaufg = np.random.choice(teilaufg, anzahl, True)
    aufgaben = {'a': einf_pp_bruchterm_multi, 'b': einf_bruchterm_multi, 'c': bruchterm_kuerz_multi,
                'd': einf_pp_bruchterm_div, 'e': einf_bruchterm_div, 'f': bruchterm_kuerz_div}

    aufg = ''
    lsg = ''
    punkte = 0
    for element in teilaufg:
        teilaufg_aufg, teilaufg_lsg = aufgaben[element]()
        aufg = aufg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_aufg
        lsg = lsg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_lsg
        if (i+1) % 4 != 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \hspace{5em} '
        elif (i + 1) % 4 == 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \\\\'
        if (i+1) % 2 != 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 2 == 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \\\\'
        else:
            pass
        punkte += 1
        i += 1

    if BE != []:
        if len(BE) > 1:
            print('Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]

def potenzgesetze(nr, anzahl=1, BE=[]):
    # Hier sollen die Schüler und Schülerinnen Logarithmusgesetze vervollständigen.
    # Mit dem Argument "anzahl=" kann die Anzahl der zufällig ausgewählten Logarithmusgesetze festgelegt werden.
    # Standardmäßig wird immer ein Gesetz erstellt.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.

    liste_bez = [f'{nr}']
    # hier wird die Funktion erstellt.
    regeln_aufgabe = {r' a^m \cdot a^n ~=~ \hspace{15em}': r' a^m \cdot a^n ~=~ a^{m+n} ',
                      r' \frac{a^m}{a^n} ~=~ \hspace{15em}': r' \frac{a^m}{a^n} ~=~ a^{m-n} ',
                      r' a^n \cdot b^n ~=~ \hspace{15em}': r' a^n \cdot b^n ~=~ \left( a \cdot b \right) ^n',
                      r' \left( a^m \right) ^n ~=~ \hspace{15em}': r' \left( a^m \right) ^n ~=~ a^{m \cdot n}',
                      r' \frac{a^n}{b^n} ~=~ \hspace{15em}': r' \frac{a^n}{b^n} ~=~ \left( \frac{a}{b} \right) ^n ',
                      r' a^0 ~=~ \hspace{15em}': r' a^0 ~=~ 1',
                      r' \frac{1}{a^n} ~=~ \hspace{15em}': r' \frac{1}{a^n} ~=~ a^{-n} ',
                      r' \sqrt[m]{a^n} ~=~ \hspace{15em}': r'\sqrt[m]{a^n} ~=~ a^{ \frac{n}{m}} '}

    exit("Die Eingabe bei anzahl muss eine Zahl sein") if type(anzahl) != int else anzahl
    anzahl = len(regeln_aufgabe) if anzahl > len(regeln_aufgabe) else anzahl
    auswahl = np.random.choice(list(regeln_aufgabe.keys()), anzahl, False)
    if anzahl == 1:
        aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
                   'Vervollständigen Sie das folgende Potenzgesetz.']
    else:
        aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
                   'Vervollständigen Sie die folgenden Potenzgesetze.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []

    aufg = lsg = ''
    for element in range(anzahl):
        if (element + 1) % 2 != 0 and (element + 1) != anzahl:
            aufg = aufg + auswahl[element]
        elif (element + 1) % 2 == 0 and (element + 1) != anzahl:
            aufg = aufg + auswahl[element] + r' \\\\'
        else:
            aufg = aufg + auswahl[element]
        lsg = lsg + regeln_aufgabe[auswahl[element]] + r' \\'

    if BE != []:
        if len(BE) > 1:
            print('Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [anzahl]
        liste_punkte = BE
    else:
        liste_punkte = [anzahl]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]

def erstes_potenzgesetz(nr, teilaufg=['a', 'b', 'c', 'd', 'e', 'f', 'g'], anzahl=False, BE=[]):
    # Hier sollen die SuS zwei Potenzen multiplizieren.
    # Mithilfe von "teilaufg=[]" können folgende Bruchterme (auch mehrfach z.B. der Form ['a', 'a', ...]) ausgewählt werden:
    # a) Potenzen mit nat. Zahlen und Exponenten
    # b) Potenzen mit nat. Zahlen und ganzz. Exponenten
    # c) Potenzen mit neg. Zahlen und ganzz. Exponenten
    # d) Potenzen mit bel. ganzen Zahlen und Exponenten
    # e) Potenzen mit Variablen und nat. Exponenten
    # f) Potenzen mit Variablen und ganzz. Exponenten
    # g) Potenzen mit Variablen, Faktoren und ganzz. Exponenten
    #
    # Mit 'anzahl=' kann eine Anzahl von zufällig ausgewählten Teilaufgaben aus den in 'teilaufg=[]' festgelegten Arten Bruchtermen erstellt werden.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.

    liste_bez = [f'{str(nr)}']
    i = 0
    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               'Vereinfache.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []

    def pos_zahl_bas_exp():
        bas = nzahl(2,6)
        exp1, exp2 = np.random.choice(range(1,5), 2, False)
        if exp1 + exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (gzahl(bas) + '^{' + gzahl(exp1) + r'} \cdot ' + gzahl(bas) + '^{' + gzahl(exp2) + '} ~')
        lsg = (gzahl(bas) + '^{' + gzahl(exp1) + r'} \cdot ' + gzahl(bas) + '^{' + gzahl(exp2) + '} ~=~ ' + gzahl(bas)
               + '^{' + gzahl(exp1) + vorz_str(exp2) + '} ~=~ ' + gzahl(bas) + '^{' + gzahl(exp1+exp2) + '}' + w_erg)
        return aufg, lsg

    def pos_zahl_bas():
        bas = nzahl(2,6)
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 + exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (gzahl(bas) + '^{' + gzahl(exp1) + r'} \cdot ' + gzahl(bas) + '^{' + gzahl(exp2) + '} ~')
        lsg = (gzahl(bas) + '^{' + gzahl(exp1) + r'} \cdot ' + gzahl(bas) + '^{' + gzahl(exp2) + '} ~=~ ' + gzahl(bas)
               + '^{' + gzahl(exp1) + vorz_str(exp2) + '} ~=~ ' + gzahl(bas) + '^{' + gzahl(exp1+exp2) + '}' + w_erg)
        return aufg, lsg

    def neg_zahl_bas():
        bas = -1 * nzahl(2,6)
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 + exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = ('(' + gzahl(bas) + ')^{' + gzahl(exp1) + r'} \cdot (' + gzahl(bas) + ')^{' + gzahl(exp2) + '} ~')
        lsg = ('(' + gzahl(bas) + ')^{' + gzahl(exp1) + r'} \cdot (' + gzahl(bas) + ')^{' + gzahl(exp2) + '} ~=~ ('
               + gzahl(bas) + ')^{' + gzahl(exp1) + vorz_str(exp2) + '} ~=~ (' + gzahl(bas) + ')^{'
               + gzahl(exp1+exp2) + '}' + w_erg)
        return aufg, lsg

    def bel_zahl_bas():
        bas = zzahl(2,6)
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 + exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (gzahl_klammer(bas) + '^{' + gzahl(exp1) + r'} \cdot ' + gzahl_klammer(bas) + '^{' + gzahl(exp2) + '} ~')
        lsg = (gzahl_klammer(bas) + '^{' + gzahl(exp1) + r'} \cdot ' + gzahl_klammer(bas) + '^{' + gzahl(exp2)
               + '} ~=~ ' + gzahl_klammer(bas) + '^{' + gzahl(exp1) + vorz_str(exp2) + '} ~=~ ' + gzahl_klammer(bas)
               + '^{' + gzahl(exp1+exp2) + '}' + w_erg)
        return aufg, lsg

    def var_bas_pos_exp():
        bas = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'])
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 + exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (bas+ '^{' + gzahl(exp1) + r'} ~ \cdot ~' + bas + '^{' + gzahl(exp2) + '} ~')
        lsg = (bas + '^{' + gzahl(exp1) + r'} \cdot ' + bas + '^{' + gzahl(exp2) + '} ~=~ ' + bas + '^{'
               + gzahl(exp1) + vorz_str(exp2) + '} ~=~ ' + bas + '^{' + gzahl(exp1+exp2) + '}' + w_erg)
        return aufg, lsg

    def var_bas_exp():
        bas = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'])
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 + exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (bas + '^{' + gzahl(exp1) + r'} \cdot ' + bas + '^{' + gzahl(exp2) + '} ~')
        lsg = (bas + '^{' + gzahl(exp1) + r'} \cdot ' + bas + '^{' + gzahl(exp2) + '} ~=~ ' + bas + '^{'
               + gzahl(exp1) + vorz_str(exp2) + '} ~=~ ' + bas + '^{' + gzahl(exp1+exp2) + '}' + w_erg)
        return aufg, lsg

    def var_bas_fakt():
        fakt1, fakt2 = faktorliste(2, 2, 12)
        bas = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'])
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 + exp2 == 0:
            w_erg = '~=~ ' + gzahl(fakt1*fakt2)
        else:
            w_erg = ''
        aufg = (gzahl(fakt1) + bas + '^{' + gzahl(exp1) + r'} \cdot '
                + gzahl_klammer(fakt2) + r'\cdot ' + bas + '^{' + gzahl(exp2) + '} ~')
        lsg = (gzahl(fakt1) + r' \cdot ' + bas + '^{' + gzahl(exp1) + r'} \cdot '
               + gzahl_klammer(fakt2) + r' \cdot ' + bas + '^{' + gzahl(exp2) + '}' + ' ~=~ ' + gzahl(fakt1)
               + r' \cdot ' + gzahl_klammer(fakt2) + r' \cdot ' + bas + '^{' + gzahl(exp1) + vorz_str(exp2)
               + '} ~=~ ' + gzahl(fakt1*fakt2) + r' \cdot ' + bas + '^{' + gzahl(exp1+exp2) + '}' + w_erg)
        return aufg, lsg

    if anzahl != False:
        if type(anzahl) != int or anzahl > 26:
            exit("Der Parameter 'anzahl=' muss eine natürliche Zahl kleiner 27 sein.")
        teilaufg = np.random.choice(teilaufg, anzahl, True)
    aufgaben = {'a': pos_zahl_bas_exp, 'b': pos_zahl_bas, 'c': neg_zahl_bas, 'd': bel_zahl_bas,
                'e': var_bas_pos_exp, 'f': var_bas_exp, 'g': var_bas_fakt}

    aufg = ''
    lsg = ''
    punkte = 0
    for element in teilaufg:
        teilaufg_aufg, teilaufg_lsg = aufgaben[element]()
        aufg = aufg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_aufg
        lsg = lsg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_lsg
        if (i+1) % 4 != 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \hspace{5em} '
        elif (i + 1) % 4 == 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \\\\'
        if (i+1) % 2 != 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 2 == 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \\\\'
        else:
            pass
        punkte += 1
        i += 1

    if BE != []:
        if len(BE) > 1:
            print('Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]
def zweites_potenzgesetz(nr, teilaufg=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], anzahl=False, BE=[]):
    # Hier sollen die SuS zwei Potenzen dividieren.
    # Mithilfe von "teilaufg=[]" können folgende Bruchterme (auch mehrfach z.B. der Form ['a', 'a', ...]) ausgewählt werden:
    # a) Potenzen mit nat. Zahlen und Exponenten
    # b) Potenzen mit nat. Zahlen und ganzz. Exponenten
    # c) Potenzen mit neg. Zahlen und ganzz. Exponenten
    # d) Potenzen mit bel. ganzen Zahlen und Exponenten
    # e) Potenzen mit Variablen und nat. Exponenten
    # f) Potenzen mit Variablen und ganzz. Exponenten
    # g) Potenzen mit Variablen, Faktoren und ganzz. Exponenten
    #
    # Mit 'anzahl=' kann eine Anzahl von zufällig ausgewählten Teilaufgaben aus den in 'teilaufg=[]' festgelegten Arten Bruchtermen erstellt werden.
    # Mit dem Parameter "BE=[]" kann die Anzahl der Bewertungseinheiten festgelegt werden. Wird hier nichts eingetragen, werden die Standardbewertungseinheiten verwendet.

    liste_bez = [f'{str(nr)}']
    i = 0
    aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
               'Vereinfache.']
    loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
    grafiken_aufgaben = []
    grafiken_loesung = []

    def pos_zahl_bas_exp():
        bas = nzahl(2,6)
        exp1, exp2 = np.random.choice(range(1,5), 2, False)
        if exp1 - exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (r' \frac{' + gzahl(bas) + '^{' + gzahl(exp1) + r'}} {' + gzahl(bas) + '^{' + gzahl(exp2) + '}} ~')
        lsg = (r' \frac{' + gzahl(bas) + '^{' + gzahl(exp1) + r'}} {' + gzahl(bas) + '^{' + gzahl(exp2) + '}} ~=~ '
               + gzahl(bas) + '^{' + gzahl(exp1) + vorz_str(-1*exp2) + '} ~=~ ' + gzahl(bas)
               + '^{' + gzahl(exp1-exp2) + '}' + w_erg)
        return aufg, lsg

    def pos_zahl_bas():
        bas = nzahl(2,6)
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 - exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (r' \frac{' + gzahl(bas) + '^{' + gzahl(exp1) + r'}} {' + gzahl(bas) + '^{' + gzahl(exp2) + '}} ~')
        lsg = (r' \frac{' + gzahl(bas) + '^{' + gzahl(exp1) + r'}} {' + gzahl(bas) + '^{' + gzahl(exp2) + '}} ~=~ '
               + gzahl(bas) + '^{' + gzahl(exp1) + vorz_str(-1*exp2) + '} ~=~ ' + gzahl(bas)
               + '^{' + gzahl(exp1-exp2) + '}' + w_erg)
        return aufg, lsg

    def neg_zahl_bas():
        bas = -1 * nzahl(2,6)
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 - exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (r' \frac{(' + gzahl(bas) + ')^{' + gzahl(exp1) + r'}} {(' + gzahl(bas) + ')^{' + gzahl(exp2) + '}} ~')
        lsg = (r' \frac{(' + gzahl(bas) + ')^{' + gzahl(exp1) + r'}} {' + gzahl(bas) + '^{' + gzahl(exp2) + '}} ~=~ ('
               + gzahl(bas) + ')^{' + gzahl(exp1) + vorz_str(-1*exp2) + '} ~=~ (' + gzahl(bas)
               + ')^{' + gzahl(exp1-exp2) + '}' + w_erg)
        return aufg, lsg

    def bel_zahl_bas():
        bas = zzahl(2,6)
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 - exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (r' \frac{' + gzahl_klammer(bas) + '^{' + gzahl(exp1) + r'}} {' + gzahl_klammer(bas) + '^{'
                + gzahl(exp2) + '}} ~')
        lsg = (r' \frac{' + gzahl_klammer(bas) + '^{' + gzahl(exp1) + r'}} {' + gzahl_klammer(bas) + '^{' + gzahl(exp2)
               + '}} ~=~ ' + gzahl_klammer(bas) + '^{' + gzahl(exp1) + vorz_str(-1*exp2) + '} ~=~ ' + gzahl_klammer(bas)
               + '^{' + gzahl(exp1-exp2) + '}' + w_erg)
        return aufg, lsg

    def var_bas_pos_exp():
        bas = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'])
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 - exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (r' \frac{' + bas + '^{' + gzahl(exp1) + r'}} {' + bas + '^{' + gzahl(exp2) + '}} ~')
        lsg = (r' \frac{' + bas + '^{' + gzahl(exp1) + r'}} {' + bas + '^{' + gzahl(exp2) + '}} ~=~ ' + bas
               + '^{' + gzahl(exp1) + vorz_str(-1*exp2) + '} ~=~ ' + bas + '^{' + gzahl(exp1-exp2) + '}' + w_erg)
        return aufg, lsg

    def var_bas_exp():
        bas = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'])
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 - exp2 == 0:
            w_erg = '~=~ 1'
        else:
            w_erg = ''
        aufg = (r' \frac{' + bas + '^{' + gzahl(exp1) + r'}} {' + bas + '^{' + gzahl(exp2) + '}} ~')
        lsg = (r' \frac{' + bas + '^{' + gzahl(exp1) + r'}} {' + bas + '^{' + gzahl(exp2) + '}} ~=~ ' + bas
               + '^{' + gzahl(exp1) + vorz_str(-1*exp2) + '} ~=~ ' + bas + '^{' + gzahl(exp1-exp2) + '}' + w_erg)
        return aufg, lsg


    def triv_var_bas_fakt():
        fakt = zzahl(2,7)
        fakt1, fakt2 = np.random.choice([fakt, fakt*zzahl(1,7)],2, False)
        bas = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'])
        exp1, exp2 = ganzz_exponenten(2,2,7, True)
        if exp1 - exp2 == 0:
            w_erg = '~=~ ' + gzahl(Rational(fakt1,fakt2))
        else:
            w_erg = ''
        aufg = (r' \frac{' + gzahl(fakt1) + '~' + bas + '^{' + gzahl(exp1) + r'}}{'
                + gzahl(fakt2) + '~' + bas + '^{' + gzahl(exp2) + '}} ~')
        lsg = (r' \frac{' + gzahl(fakt1) + bas + '^{' + gzahl(exp1) + r'}}{' + gzahl(fakt2) + '~' + bas + '^{'
               + gzahl(exp2) + '}} ~=~ ' + gzahl(Rational(fakt1,fakt2)) + r' \cdot ' + bas + '^{' + gzahl(exp1)
               + vorz_str(-1*exp2) + '} ~=~ ' + vorz_v_aussen(Rational(fakt1,fakt2), bas + '^{' + gzahl(exp1-exp2)+ '}')
               + w_erg)
        return aufg, lsg

    def einf_var_bas_fakt():
        zaehler, nenner = np.random.choice([2,3,5,7,9,11],2, False)
        fakt_erw = zzahl(2, 10)
        fakt1, fakt2 = np.random.choice([zaehler*fakt_erw, nenner * fakt_erw], 2, False)
        bas = np.random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'],2,False)
        bas.sort()
        bas1, bas2 = bas
        exp1, exp2, exp3, exp4 = ganzz_exponenten(4,2,8, True)
        if exp1 - exp3 == 0 or exp2 - exp4 == 0:
            w_erg = ' ~=~ ' + gzahl(Rational(fakt1, fakt2))
            if exp1 - exp3 != 0:
                w_erg = w_erg + bas1 + '^{' + gzahl(exp1 - exp3) + '}'
            if exp2 - exp4 != 0:
                w_erg = w_erg + bas2 + '^{' + gzahl(exp2 - exp4) + '}'
        else:
            w_erg = ''
        aufg = (r' \frac{' + gzahl(fakt1) + '~' + bas1 + '^{' + gzahl(exp1) + r'}' + bas2 + '^{' + gzahl(exp2) + r'}}{'
                + gzahl(fakt2) + '~' + bas1 + '^{' + gzahl(exp3) + '}' + bas2 + '^{' + gzahl(exp4) + '}} ~')
        lsg = (r' \frac{' + gzahl(fakt1) + '~' + bas1 + '^{' + gzahl(exp1) + r'}' + bas2 + '^{' + gzahl(exp2) + r'}}{'
                + gzahl(fakt2) + '~' + bas1 + '^{' + gzahl(exp3) + '}' + bas2 + '^{' + gzahl(exp4) + r'}} ~=~ \frac{'
               + gzahl(fakt1) + '}{' + gzahl(fakt2) + r'} \cdot ' + bas1 + '^{' + gzahl(exp1) + vorz_str(-1 * exp3)
               + '}' + bas2 + '^{' + gzahl(exp2) + vorz_str(-1 * exp4) + '} ~=~ ' + gzahl(Rational(fakt1, fakt2))
               + '~' + bas1 + '^{' + gzahl(exp1 - exp3) + '}' + bas2 + '^{' + gzahl(exp2 - exp4) + '}' + w_erg)
        return aufg, lsg

    def nor_var_bas_fakt():
        ausw_bruch = np.random.choice([2,3,5,7,9,11], 2, False)
        zaehler, nenner = random.choice([-1,1])*ausw_bruch[0], random.choice([-1,1])*ausw_bruch[1]
        erw1, erw2 = nzahl(2,10), nzahl(5,12)
        zaehler1, nenner2, zaehler2, nenner1 = zaehler*erw1, erw1, erw2, nenner*erw2
        bas = np.random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x', 'y', 'z'],4,False)
        bas.sort()
        bas1, bas2, bas3, bas4 = bas
        list_exp = ganzz_exponenten(8,2,12, True)
        exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8 = list_exp
        list_exp_diff = [exp1 - exp3, exp2 - exp4, exp5 - exp7, exp6 - exp8]
        exp_diff1, exp_diff2, exp_diff3, exp_diff4 = list_exp_diff
        if 0 in list_exp_diff:
            w_erg = ' ~=~ ' + gzahl(Rational(zaehler, nenner))
            n = 0
            for element in list_exp_diff:
                if element != 0:
                    w_erg = w_erg + bas[n] + '^{' + gzahl(element) + '}'
                n += 1
        else:
            w_erg = ''
        aufg = (r' \frac{' + gzahl(fakt1) + '~' + bas1 + '^{' + gzahl(exp1) + r'}' + bas2 + '^{' + gzahl(exp2) + r'}}{'
                + gzahl(fakt2) + '~' + bas1 + '^{' + gzahl(exp3) + '}' + bas2 + '^{' + gzahl(exp4) + '}} ~')
        lsg = (r' \frac{' + gzahl(fakt1) + '~' + bas1 + '^{' + gzahl(exp1) + r'}' + bas2 + '^{' + gzahl(exp2) + r'}}{'
                + gzahl(fakt2) + '~' + bas1 + '^{' + gzahl(exp3) + '}' + bas2 + '^{' + gzahl(exp4) + r'}} ~=~ \frac{'
               + gzahl(fakt1) + '}{' + gzahl(fakt2) + r'} \cdot ' + bas1 + '^{' + gzahl(exp1) + vorz_str(-1 * exp3)
               + '}' + bas2 + '^{' + gzahl(exp2) + vorz_str(-1 * exp4) + '} ~=~ ' + gzahl(Rational(fakt1, fakt2))
               + '~' + bas1 + '^{' + gzahl(exp1 - exp3) + '}' + bas2 + '^{' + gzahl(exp2 - exp4) + '}' + w_erg)
        return aufg, lsg

    if anzahl != False:
        if type(anzahl) != int or anzahl > 26:
            exit("Der Parameter 'anzahl=' muss eine natürliche Zahl kleiner 27 sein.")
        teilaufg = np.random.choice(teilaufg, anzahl, True)
    aufgaben = {'a': pos_zahl_bas_exp, 'b': pos_zahl_bas, 'c': neg_zahl_bas, 'd': bel_zahl_bas,
                'e': var_bas_pos_exp, 'f': var_bas_exp, 'g': triv_var_bas_fakt, 'h': einf_var_bas_fakt}

    aufg = ''
    lsg = ''
    punkte = 0
    for element in teilaufg:
        teilaufg_aufg, teilaufg_lsg = aufgaben[element]()
        aufg = aufg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_aufg
        lsg = lsg + str(liste_teilaufg[i]) + r') \quad ' + teilaufg_lsg
        if (i+1) % 4 != 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \hspace{5em} '
        elif (i + 1) % 4 == 0 and i+1 < len(teilaufg):
            aufg = aufg + r' \\\\'
        if (i+1) % 2 != 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \hspace{5em} '
        elif (i + 1) % 2 == 0 and i+1 < len(teilaufg):
            lsg = lsg + r' \\\\'
        else:
            pass
        punkte += 1
        i += 1

    if BE != []:
        if len(BE) > 1:
            print('Der Parameter BE darf nur ein Element haben, zum Beispiel BE=[2]. '
                  'Deswegen wird die standardmäßige Punkteverteilung übernommen.')
            liste_punkte = [punkte]
        liste_punkte = BE
    else:
        liste_punkte = [punkte]
    aufgabe.append(aufg)
    loesung.append(lsg)

    return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung, liste_punkte, liste_bez]


