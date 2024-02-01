import datetime
import string
import numpy as np
import random, math
import matplotlib.pyplot as plt
from numpy.linalg import solve as slv
from pylatex import (Document, NoEscape, SmallText, LargeText, MediumText, NewPage, Tabular, Alignat, Figure,
                     MultiColumn, MultiRow, Package)
from pylatex.utils import bold
from sympy import *
from plotten import Graph
# Definition der Funktionen

a, b, c, d, e, f, g, h, x, y, z = symbols('a b c d e f g h x y z')
liste_teilaufg = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
nr_aufgabe = 0

def zzahl(p, q):
    return random.choice([-1, 1]) * random.randint(p, q)

def nzahl(p, q):
    return random.randint(p, q)

def gzahl(k):
    if k%1 == 0:
        return latex(int(k))
    else:
        return latex(k)

def vorz(k):
    if k < 0:
        return '-'
    else:
        return '+'

def vorz_fakt(k):
    if k < 0:
        return -1
    else:
        return 1

def vorz_str(k):
    if k%1 == 0:
        k = int(k)
    if k < 0:
        return latex(k)
    else:
        return f'+{latex(k)}'

def vorz_str_minus(k):
    if k%1 == 0:
        k = int(k)
    if k < 0:
        return f'({latex(k)})'
    else:
        return latex(k)

def vektor_rational(vec,p):
    vec_p = [element*p for element in vec]
    print(vec_p)
    k = 0
    for element in vec_p:
        if element % 1 == 0:
            k += 1
    if k == 3:
        return True
    else:
        return False

def erstellen(Teil):
    print(f'\033[38;2;100;141;229m\033[1m{Teil}\033[0m')
    liste_bez = ['Aufgabe']
    liste_punkte = ['Punkte']


    def punkt_vektor(p):
        return np.array([zzahl(1,p), zzahl(1,p), zzahl(1,p)])

    def faktorliste(n, p=1,q=10):
        return [zzahl(p, q) for _ in range(n)]  # mit dem _ kann man die Variable weglassen

    def vektor_runden(vec,p):
        return [N(elements,p) for elements in vec]
    # Berechnung für die Aufgaben
    def vektor_ganzzahl(vec):
        return np.array([int(element) if element % 1 == 0 else element for element in vec])

    def vektor_kürzen(vec, p = 50):
        faktor = [x + 1 for x in range(p)]
        list = np.array(vec)
        i = 0
        for element in vec:
            k = 0
            if list[i] % 1 == 0:
                i += 1
            else:
                while (list[i] * faktor[k]) % 1 != 0 and k+1 < p:
                    k += 1
                list = list * faktor[k]
                i += 1
        # print('erweitert: ' + str(list))
        teiler = [x + 1 for x in range(int(max(list)/2))]
        for zahl in teiler:
            treffer = [1 for x in list if x % zahl == 0]
            if sum(treffer) == len(vec):
                list = list / zahl
        # print('gekürzt: ' + str(list))
        list = np.array([int(element) if element % 1 == 0 else element for element in list])
        return np.array(list)

    def punkte_ebene(nr, teilaufg):
        i = 0
        v_teiler = zzahl(1, 3)
        punkt_a = [ax, ay, az] = punkt_vektor(3)  # Punkt A liegt auf Gerade g_1
        v = [vx, vy, vz] = vektor_ganzzahl(np.array([zzahl(1, 6) / 2 * v_teiler,
                                                     zzahl(1, 6) / 2 * v_teiler,
                                                     v_teiler]))  # Vektor v ist der Richtungsvektor von Geraden g_1
        # Vektor u steht orthogonal auf v
        ux, uy = zzahl(1, 3), zzahl(1, 3)  # x und y Koordinate von u kann frei gewählt werden
        uz = - 1 * (vx * ux + vy * uy) / vz
        u = vektor_ganzzahl([ux, uy, uz])
        punkt_b = [bx, by, bz] = vektor_ganzzahl(punkt_a + v)  # Punkte C und D liegen auf h
        punkt_c = [cx, cy, cz] = vektor_ganzzahl(punkt_b + zzahl(1, 4) * np.array(u))
        w = vektor_ganzzahl(punkt_c - punkt_a)  # Vektor w ist der Richtungsvektor von h
        [wx, wy, wz] = vektor_runden(w, 3)
        n = [nx, ny, nz] = vektor_ganzzahl(np.cross(v, w))
        n_gk = [nx_gk, ny_gk, nz_gk] = vektor_kürzen(n)
        if 'a' in teilaufg:
            aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),'Gegeben sind die Punkte '
                       'A( ' + gzahl(ax) + ' | ' + gzahl(ay) + ' | ' + gzahl(az) + ' ), ' 
                       'B( ' + gzahl(bx) + ' | ' + gzahl(by) + ' | ' + gzahl(bz) + ' ) und '
                       'C( ' + gzahl(cx) + ' | ' + gzahl(cy) + ' | ' + gzahl(cz) + ' ).  \n\n']
        elif 'b' in teilaufg and 'a' not in teilaufg:
            aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
                       r' \mathrm{Gegeben~ist~die~Ebene} \quad E: \overrightarrow{x} ~=~ \begin{pmatrix} '
                       + gzahl(ax) + r' \\' + gzahl(ay) + r' \\' + gzahl(az) + r' \\'
                       r' \end{pmatrix} ~+~r \cdot \begin{pmatrix} '
                       + gzahl(bx - ax) + r' \\' + gzahl(by - ay) + r' \\' + gzahl(bz - az) + r' \\'
                       r' \end{pmatrix} ~+~ s \cdot \begin{pmatrix}'
                       + gzahl(cx - ax) + r' \\' + gzahl(cy - ay) + r' \\' + gzahl(cz - az) + r' \\'
                       r' \end{pmatrix}']
        elif 'a' and 'b' not in teilaufg:
            aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')),
                       r' \mathrm{Gegeben~ist~die~Ebene} \quad E: \begin{bmatrix} \overrightarrow{x}'
                       r'~-~ \begin{pmatrix} ' + gzahl(ax) + r' \\' + gzahl(ay) + r' \\' + gzahl(az) + r' \\'
                       r' \end{pmatrix} \end{bmatrix} \cdot \begin{pmatrix} '
                       + gzahl(nx_gk) + r' \\' + gzahl(ny_gk) + r' \\' + gzahl(nz_gk) + r' \\'
                       r' \end{pmatrix} ~=~0']
        loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
        grafiken_aufgaben = ['','']
        grafiken_loesung = ['']

        if 'a' in teilaufg:
            punkte_aufg = 5
            liste_punkte.append(punkte_aufg)
            liste_bez.append(str(nr) + '. ' + str(liste_teilaufg[i]) + ')')
            grafiken_aufgaben.append(f'Aufgabe_{nr}{liste_teilaufg[i]}')
            grafiken_loesung.append(f'Loesung_{nr}{liste_teilaufg[i]}')

            aufgabe.append(str(teilaufg[i]) + f') Stellen Sie die Parametergleichung der Ebene E auf, '
                                              f'welche die Punkte A, B und C enthält. \n\n')
            loesung.append(str(teilaufg[i]) + r') \quad \overrightarrow{AB} ~=~ \begin{pmatrix} '
                           + gzahl(bx-ax) + r' \\' + gzahl(by-ay) + r' \\' + gzahl(bz-az) + r' \\'
                           r' \end{pmatrix} \quad \mathrm{und} \quad \overrightarrow{AC} ~=~ \begin{pmatrix} '
                           + gzahl(cx-ax) + r' \\' + gzahl(cy-ay) + r' \\' + gzahl(cz-az) + r' \\'
                           r' \end{pmatrix} \quad \to \quad E: \overrightarrow{x} ~=~ \begin{pmatrix} '
                           + gzahl(ax) + r' \\' + gzahl(ay) + r' \\' + gzahl(az) + r' \\'
                           r' \end{pmatrix} ~+~r \cdot \begin{pmatrix} '
                           + gzahl(bx - ax) + r' \\' + gzahl(by - ay) + r' \\' + gzahl(bz - az) + r' \\'
                           r' \end{pmatrix} ~+~ s \cdot \begin{pmatrix}'
                           + gzahl(cx - ax) + r' \\' + gzahl(cy - ay) + r' \\' + gzahl(cz - az) + r' \\'
                           r' \end{pmatrix} \quad (5P) \\'
                           r' \mathrm{insgesamt~' + str(punkte_aufg) + r'~Punkte} \\')
            i += 1

        if 'b' in teilaufg:
            punkte_aufg = 7
            liste_punkte.append(punkte_aufg)
            liste_bez.append(str(nr) + '. ' + str(liste_teilaufg[i]) + ')')
            grafiken_aufgaben.append(f'Aufgabe_{nr}{liste_teilaufg[i]}')
            grafiken_loesung.append(f'Loesung_{nr}{liste_teilaufg[i]}')

            aufgabe.append(str(teilaufg[i]) + f') Formen Sie die Gleichung für Ebene E in '
                                              f'Normalen- und Koordinatenform um. \n\n')
            loesung.append(str(teilaufg[i]) + r') \quad \overrightarrow{n} ~=~ \begin{pmatrix} '
                           + gzahl(vy * wz) + '-' + vorz_str_minus(vz * wy) + r' \\'
                           + gzahl(vz * wx) + '-' + vorz_str_minus(vx * wz) + r' \\'
                           + gzahl(vx * wy) + '-' + vorz_str_minus(vy * wx) + r' \\ \end{pmatrix} ~=~ \begin{pmatrix} '
                           + gzahl(nx) + r' \\' + gzahl(ny) + r' \\' + gzahl(nz) + r' \\'
                           + r' \end{pmatrix} ~=~ ' + gzahl(Rational(ny,ny_gk)) + r' \cdot \begin{pmatrix} '
                           + gzahl(nx_gk) + r' \\' + gzahl(ny_gk) + r' \\' + gzahl(nz_gk) + r' \\'
                           + r' \end{pmatrix} \quad (3P) \\\\'
                           + r'E: \begin{bmatrix} \overrightarrow{x} ~-~ \begin{pmatrix} '
                           + gzahl(ax) + r' \\' + gzahl(ay) + r' \\' + gzahl(az) + r' \\'
                           + r' \end{pmatrix} \end{bmatrix} \cdot \begin{pmatrix} '
                           + gzahl(nx_gk) + r' \\' + gzahl(ny_gk) + r' \\' + gzahl(nz_gk) + r' \\'
                           + r' \end{pmatrix} ~=~0 \quad (2P) \\\\ E:~' + gzahl(nx_gk) + r' \cdot x'
                           + vorz_str(ny_gk) + r' \cdot y' + vorz_str(nz_gk) + r' \cdot z' + '~=~'
                           + gzahl(np.dot(punkt_a, n_gk)) + r' \quad (2P) \\'
                           + r' \mathrm{insgesamt~' + str(punkte_aufg) + r'~Punkte} \\')
            i += 1

        if 'c' in teilaufg:
            parameter_r = zzahl(1,4)
            parameter_s = zzahl(1,4)
            auswahl = random.choice([0,1])
            if auswahl == 0:
                punkt_t = [tx, ty, tz] = vektor_ganzzahl(punkt_c + parameter_r * np.array(v)
                                        + parameter_s * np.array(w))
            else:
                punkt_t = [tx, ty, tz] = vektor_ganzzahl(punkt_c + parameter_r * np.array(v)
                                        + parameter_s * np.array(w) + zzahl(1, 7) / 2 * np.array(n_gk))
            if np.array_equal(punkt_t, punkt_c + parameter_r * v + parameter_s * w):
                lsg = r' \quad \mathrm{w.A.} \\ \mathrm{Der~Punkt~T~liegt~auf~der~Geraden.} \quad (3P) \\'
            else:
                lsg = r' \quad \mathrm{f.A.} \\ \mathrm{Der~Punkt~T~liegt~nicht~auf~der~Geraden.} \quad (3P) \\'
            punkte_aufg = 3

            liste_punkte.append(punkte_aufg)
            liste_bez.append(str(nr) + '. ' + str(liste_teilaufg[i]) + ')')
            grafiken_aufgaben.append('')
            grafiken_aufgaben.append(f'Aufgabe_{nr}{liste_teilaufg[i]}')
            grafiken_loesung.append(f'Loesung_{nr}{liste_teilaufg[i]}')
            aufgabe.append('Gegeben ist ein weiterer Punkt T( ' + gzahl(tx) + ' | ' + gzahl(ty) + ' | '
                           + gzahl(tz) + ' ), \n\n')
            aufgabe.append(str(teilaufg[i]) + f') Überprüfen Sie, ob der Punkt T in der Ebene E liegt. \n\n')
            loesung.append(str(teilaufg[i]) + (r') \quad E:~' + gzahl(nx_gk) + r' \cdot (' + gzahl(tx) + ')'
                                               + vorz_str(ny_gk) + r' \cdot (' + gzahl(ty) + ')'
                                               + vorz_str(nz_gk) + r' \cdot (' + gzahl(tz) + ') ~=~'
                                               + gzahl(np.dot(punkt_a, n_gk)) + r' \quad \to \quad '
                                               + gzahl(np.dot(n_gk, punkt_t)) + '~=~'
                                               + gzahl(np.dot(punkt_a, n_gk)) + lsg
                                               + r' \mathrm{insgesamt~' + str(punkte_aufg) + r'~Punkte} \\'))
            i += 1
        return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung]
    def gerade_ebene(nr, teilaufg):
        i = 0
        v_teiler = zzahl(1, 3)
        punkt_a = [ax, ay, az] = punkt_vektor(3)  # Punkt A liegt in Ebene E
        v = [vx, vy, vz] = vektor_ganzzahl(np.array([zzahl(1, 6) / 2 * v_teiler,
                                                     zzahl(1, 6) / 2 * v_teiler,
                                                     v_teiler]))  # Vektor v ist der Richtungsvektor von Geraden g_1
        # Vektor u steht orthogonal auf v
        ux, uy = zzahl(1, 3), zzahl(1, 3)  # x und y Koordinate von u kann frei gewählt werden
        uz = - 1 * (vx * ux + vy * uy) / vz
        u = vektor_ganzzahl([ux, uy, uz])
        punkt_b = [bx, by, bz] = vektor_ganzzahl(punkt_a + v)  # Punkte C und D liegen auf h
        punkt_c = [cx, cy, cz] = vektor_ganzzahl(punkt_b + zzahl(1, 4) * np.array(u))
        w = vektor_ganzzahl(punkt_c - punkt_a)  # Vektor w ist der Richtungsvektor von h
        [wx, wy, wz] = vektor_runden(w, 3)
        n = [nx, ny, nz] = vektor_ganzzahl(np.cross(v, w))
        n_gk = [nx_gk, ny_gk, nz_gk] = vektor_kürzen(n)

        print('a: ' + str(punkt_a))
        print('b: ' + str(punkt_b))
        print('c: ' + str(punkt_c))
        print('vektor v: ' + str(v))
        print('vektor u: ' + str(u))
        print('vektor w: ' + str(w))
        print('vektor n: ' + str(n))
        print('vektor n_gk: ' + str(n_gk))

        aufgabe = [MediumText(bold('Aufgabe ' + str(nr) + ' \n\n')), 'Gegeben ist die Ebene E in der Koordinatenform',
                   r' E:~' + gzahl(nx_gk) + 'x' + vorz_str(ny_gk) + 'y'
                   + vorz_str(nz_gk) + 'z ~=~' + gzahl(np.dot(punkt_a,n_gk))]
        loesung = [r' \mathbf{Lösung~Aufgabe~}' + str(nr) + r' \hspace{35em}']
        grafiken_aufgaben = ['', '']
        grafiken_loesung = ['']

        if 'a' in teilaufg:
            punkte_aufg = 5
            liste_bez.append(str(nr) + '. ' + str(liste_teilaufg[i]) + ')')
            grafiken_aufgaben.append(f'Aufgabe_{nr}{liste_teilaufg[i]}')
            grafiken_loesung.append(f'Loesung_{nr}{liste_teilaufg[i]}')

            auswahl = random.choice(['identisch', 'parallel', 'schneiden'])
            # auswahl = 'schneiden'
            if auswahl == 'identisch':
                punkt_e = [ex, ey, ez] = vektor_ganzzahl(punkt_a + zzahl(1, 7) / 2 * np.array(v))
                punkt_f = [fx, fy, fz] = vektor_ganzzahl(punkt_b + zzahl(1, 7) / 2 * np.array(w))
                g_v = [g_vx, g_vy, g_vz] = np.array([fx - ex, fy - ey, fz - ez])
                lsg = (gzahl(nx_gk * ex + ny_gk * ey + nz_gk * ez) + '~=~'
                       + gzahl(np.dot(punkt_a,n_gk))
                       + r' \quad \mathrm{w.A. \quad Die~Gerade~liegt~in~der~Ebene. \quad (2P) } \\')
            elif auswahl == 'parallel':
                abstand = zzahl(1, 7) / 2 * np.array(n_gk)
                punkt_e = [ex, ey, ez] = vektor_ganzzahl(punkt_a + zzahl(1, 7) / 2 * np.array(v) + abstand)
                punkt_f = [fx, fy, fz] = vektor_ganzzahl(punkt_b + zzahl(1, 7) / 2 * np.array(w) + abstand)
                g_v = [g_vx, g_vy, g_vz] = np.array([fx - ex, fy - ey, fz - ez])
                lsg = (gzahl(nx_gk * ex + ny_gk * ey + nz_gk * ez) + '~=~'
                       + gzahl(np.dot(punkt_a, n_gk))
                       + r' \quad \mathrm{f.A. \quad Die~Gerade~ist~parallel~zur~Ebene. \quad (2P)} \\')
            else:
                g_v = [1/7,1/3,1/5]
                while vektor_rational(g_v,10) != True:
                    punkt_s = [sx, sy, sz] = vektor_ganzzahl(punkt_a + zzahl(1, 3) * np.array(v))
                    punkt_t = vektor_ganzzahl(punkt_a + zzahl(1, 5)/2 * np.array(n_gk))
                    g_v = [g_vx, g_vy, g_vz] = punkt_t - punkt_s
                    ergebnis_r = zzahl(1, 6) / 2
                    punkt_e = [ex, ey, ez] = punkt_s - ergebnis_r * g_v
                    punkt_f = [fx, fy, fz] = punkt_e - vorz_fakt(ergebnis_r)*g_v


                lsg = (gzahl(nx_gk * ex + ny_gk * ey + nz_gk * ez)
                       + vorz_str(nx_gk * g_vx + ny_gk * g_vy + nz_gk * g_vz) + r' \cdot r ~=~'
                       + gzahl(np.dot(punkt_a, n_gk)) + r' \quad \vert '
                       + vorz_str(-1 * (nx_gk * ex + ny_gk * ey + nz_gk * ez)) + r' \quad \vert \div '
                       + vorz_str_minus(nx_gk * g_vx + ny_gk * g_vy + nz_gk * g_vz) + r' \quad \to \quad r~=~'
                       + gzahl(ergebnis_r) + r' \quad (2P) \\'
                       + r' \mathrm{Die~Gerade~schneidet~die~Ebene~im~Punkt:} \\ \begin{pmatrix} '
                       + gzahl(ex) + r' \\' + gzahl(ey) + r' \\' + gzahl(ez) + r' \\'
                       r' \end{pmatrix}' + vorz_str(ergebnis_r) + r' \cdot \begin{pmatrix} '
                       + gzahl(g_vx) + r' \\' + gzahl(g_vy) + r' \\' + gzahl(g_vz) + r' \\'
                       r' \end{pmatrix} ~=~ \begin{pmatrix} '
                       + gzahl(ex + ergebnis_r*g_vx) + r' \\' + gzahl(ey + ergebnis_r*g_vy) + r' \\'
                       + gzahl(ez + ergebnis_r*g_vz) + r' \\ \end{pmatrix} \quad \to \quad S('
                       + gzahl(ex + ergebnis_r*g_vx) + r' \vert ' + gzahl(ey + ergebnis_r*g_vy) + r' \vert '
                       + gzahl(ez + ergebnis_r*g_vz) + r') \quad (3P) \\')


                punkte_aufg += 3



            print('punkt_s: ' + str(punkt_s))
            print('punkt_f: ' + str(punkt_f))
            print('Vektor g_v: ' + str(g_v))
            print('r: ' + str(ergebnis_r))
            print('punkt_e: ' + str(punkt_e))

            aufgabe.extend(('und die Punkte: A( ' + gzahl(ex) + ' | ' + gzahl(ey) + ' | ' + gzahl(ez) + ' ) und ' 
                            'B( ' + gzahl(fx) + ' | ' + gzahl(fy) + ' | ' + gzahl(fz) + ' ).  \n\n',
                            str(teilaufg[i]) + f') Überprüfe die Lagebeziehung der Geraden, die A und B enthält, '
                                               f'zur Ebene E. Berechne ggf. den Schnittpunkt. \n\n'))
            loesung.append(str(teilaufg[i]) + r') \quad \overrightarrow{AB} ~=~ \begin{pmatrix} '
                           + gzahl(g_vx) + r' \\' + gzahl(g_vy) + r' \\' + gzahl(g_vz) + r' \\'
                           r' \end{pmatrix} \quad \to \quad g: \overrightarrow{x} \ ~=~ \begin{pmatrix} '
                           + gzahl(ex) + r' \\' + gzahl(ey) + r' \\' + gzahl(ez) + r' \\'
                           r' \end{pmatrix} ~+~r \cdot \begin{pmatrix} '
                           + gzahl(g_vx) + r' \\' + gzahl(g_vy) + r' \\' + gzahl(g_vz) + r' \\'
                           r' \end{pmatrix} \quad (2P) \\ '
                           + gzahl(nx_gk) + r' \cdot (' + gzahl(ex) + vorz_str(g_vx) + 'r)'
                           + vorz_str(ny_gk) + r' \cdot (' + gzahl(ey) + vorz_str(g_vy) + 'r)'
                           + vorz_str(nz_gk) + r' \cdot (' + gzahl(ez) + vorz_str(g_vz) + 'r) ~=~'
                           + gzahl(np.dot(punkt_a,n_gk)) + r' \quad (1P) \\'
                           + lsg + r' \mathrm{insgesamt~' + str(punkte_aufg) + r'~Punkte} \\')
            liste_punkte.append(punkte_aufg)
            i += 1

        return [aufgabe, loesung, grafiken_aufgaben, grafiken_loesung]


    aufgaben = [punkte_ebene(1, ['a', 'b', 'c']),
                gerade_ebene(2,['a'])]

    # erstellen der Tabelle zur Punkteübersicht
    Punkte = (sum(liste_punkte[1:]))
    liste_bez.append('Summe')
    liste_punkte.append(str(Punkte))
    anzahl_spalten = len(liste_punkte)
    liste_ergebnis_z1 = ['erhaltene']
    for p in range(anzahl_spalten - 1):
        liste_ergebnis_z1.append('')
    liste_ergebnis_z2 = ['Punkte']
    for p in range(anzahl_spalten - 1):
        liste_ergebnis_z2.append('')

    spalten = '|'
    for p in liste_punkte:
        spalten += 'c|'

    table2 = Tabular(spalten, row_height=1.2)
    table2.add_hline()
    table2.add_row((MultiColumn(anzahl_spalten, align='|c|', data='Punkteverteilung aller Aufgaben'),))
    table2.add_hline()
    table2.add_row(liste_bez)
    table2.add_hline()
    table2.add_row(liste_punkte)
    table2.add_hline()
    table2.add_row(liste_ergebnis_z1)
    table2.add_row(liste_ergebnis_z2)
    table2.add_hline()

    # Angaben für den Test im pdf-Dokument
    Datum = datetime.date.today().strftime('%d.%m.%Y')
    Kurs = 'Grundkurs'
    Fach = 'Mathematik'
    Klasse = '13'
    Lehrer = 'Herr Herrys'
    Art = '9. Hausaufgabenkontrolle'
    Titel = 'Lagebeziehung Gerade Ebene'

    # der Teil in dem die PDF-Datei erzeugt wird
    def Hausaufgabenkontrolle():
        geometry_options = {"tmargin": "0.2in", "lmargin": "1in", "bmargin": "0.4in", "rmargin": "0.7in"}
        Aufgabe = Document(geometry_options=geometry_options)
        Aufgabe.packages.append(Package('amsfonts'))  # fügt das Package 'amsfonts' hinzu, für das \mathbb{R} für reelle Zahlen
        # erste Seite
        table1 = Tabular('|c|c|c|c|c|c|', row_height=1.2)
        table1.add_row((MultiColumn(6, align='c', data=MediumText(bold('Torhorst - Gesamtschule'))),))
        table1.add_row((MultiColumn(6, align='c', data=SmallText(bold('mit gymnasialer Oberstufe'))),))
        table1.add_hline()
        table1.add_row('Klasse:', 'Fach:', 'Niveau:', 'Lehrkraft:', 'Datum:', 'Art:')
        table1.add_hline()
        table1.add_row(Klasse, Fach, Kurs, Lehrer, Datum, Art)
        table1.add_hline()
        Aufgabe.append(table1)
        Aufgabe.append(' \n\n\n\n')
        Aufgabe.append(LargeText(bold(f' {Titel} \n\n')))
        for aufgabe in aufgaben:
            k = 0
            for elements in aufgabe[0]:
                if '~' in elements:
                    with Aufgabe.create(Alignat(aligns=1, numbering=False, escape=False)) as agn:
                        agn.append(elements)
                elif 'Abbildung' in elements:
                    Aufgabe.append(elements)
                    with Aufgabe.create(Figure(position='h!')) as graph:
                        graph.add_image(aufgabe[2][k], width='200px')
                else:
                    Aufgabe.append(elements)
                k += 1

        Aufgabe.append('\n\n')
        Aufgabe.append(table2)

        Aufgabe.append(NewPage())
        Aufgabe.append(LargeText(bold(Teil + ' - bearbeitet von:')))

        Aufgabe.generate_pdf(f'Ma {Klasse} - {Art} {Teil}', clean_tex=true)
        print('\033[38;2;0;220;120m\033[1mKontrolle erstellt\033[0m')

    # Erwartungshorizont
    def Erwartungshorizont():
        geometry_options = {"tmargin": "0.4in", "lmargin": "1in", "bmargin": "1in", "rmargin": "1in"}
        Loesung = Document(geometry_options=geometry_options)
        Loesung.packages.append(Package('amsfonts'))
        Loesung.append(LargeText(bold(f'Loesung für {Art} {Teil} \n\n {Titel} \n\n')))

        for loesung in aufgaben:
            k = 0
            for elements in loesung[1]:
                if '~' in elements:
                    with Loesung.create(Alignat(aligns=2, numbering=False, escape=False)) as agn:
                        agn.append(elements)
                elif 'Abbildung' in elements:
                    Loesung.append(elements)
                    with Loesung.create(Figure(position='h!')) as graph:
                        graph.add_image(loesung[3][k], width='200px')
                else:
                    Loesung.append(elements)
                k += 1
        Loesung.append(MediumText(bold(f'insgesamt {Punkte} Punkte')))

        Loesung.generate_pdf(f'Ma {Klasse} - {Art} {Teil} - Lsg', clean_tex=true)
        print('\033[38;2;0;220;120m\033[1mErwartungshorizont erstellt\033[0m')

    # Druck der Seiten
    Hausaufgabenkontrolle()
    Erwartungshorizont()


anzahl_Arbeiten = 2
probe = False
alphabet = string.ascii_uppercase
for teil_id in range(anzahl_Arbeiten):
    if probe:
        erstellen('Probe {:02d}'.format(teil_id + 1))
    else:
        erstellen(f'Gr. {alphabet[teil_id]}')
    print()  # Abstand zwischen den Arbeiten (im Terminal)
