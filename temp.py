import random

from sympy import *
from skripte.funktionen import *

a, b, c, d, e, f, g, h, x, y, z = symbols('a b c d e f g h x y z')

# b = list(range(1,4))
# print(b)
#
# i = 0
# for m in range(1,7):
#     for n in range(1,7):
#         if m + n > 9:
#             print ('m: ' + str(m) + ' und n: ' + str(n) + ' und m+n:' + str(m+n))
#             i += 1
# print(i)
# a = [[1,2],[2,3]]


# teilaufg = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'i']
# liste_teilaufg = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
# if len([element for element in teilaufg if element in liste_teilaufg[8:11]]) > 0:
#     if len([element for element in teilaufg if element in liste_teilaufg[0:7]]) > 0:
#         print([element for element in teilaufg if element in liste_teilaufg[8:11]])
#         print([element for element in teilaufg if element in liste_teilaufg[0:7]])

# print('seite_' + str(i for i in range(1,2)))

# wert = 123.3
# wert_neu = str(wert).replace('.', ',')

nst_12 = nzahl(1,3)
nst_34 = nst_12 + nzahl(2,3)
faktor = zzahl(1,7)/2
fkt = collect(expand(faktor*(x**2-nst_12)*(x**2-nst_34)),x)
lsg_nst = solve(fkt,x)
fkt_1 = diff(fkt,x)
lsg_extrema = solve(fkt_1,x)
print(fkt)
print(lsg_nst)
print(fkt_1)
print(lsg_extrema)

print(collect(expand(a*(x**2-b)*(x**2-c)),x))
