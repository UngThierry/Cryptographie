# Sorbonne Université LU3IN024 2021-2022
# TME 5 : Cryptographie à base de courbes elliptiques
#
# Etudiant.e 1 : UNG 3804472
# Etudiant.e 2 : NOM ET NUMERO D'ETUDIANT

from math import sqrt
import matplotlib.pyplot as plt
from random import randint

# Fonctions utiles


def exp(a, N, p):
    """Renvoie a**N % p par exponentiation rapide.
    """
    def binaire(N):
        L = list()
        while (N > 0):
            L.append(N % 2)
            N = N // 2
        L.reverse()
        return L
    res = 1
    for Ni in binaire(N):
        res = (res * res) % p
        if Ni == 1:
            res = (res * a) % p
    return res


def factor(n):
    """ Return the list of couples (p, a_p) where p is a prime divisor of n and
    a_p is the p-adic valuation of n.
    """
    def factor_gen(n):
        j = 2
        while n > 1:
            for i in range(j, int(sqrt(n)) + 1):
                if n % i == 0:
                    n //= i
                    j = i
                    yield i
                    break
            else:
                if n > 1:
                    yield n
                    break

    factors_with_multiplicity = list(factor_gen(n))
    factors_set = set(factors_with_multiplicity)

    return [(p, factors_with_multiplicity.count(p)) for p in factors_set]


def inv_mod(x, p):
    """Renvoie l'inverse de x modulo p.
    """
    return exp(x, p - 2, p)


def racine_carree(a, p):
    """Renvoie une racine carrée de a mod p si p = 3 mod 4.
    """
    assert p % 4 == 3, "erreur: p != 3 mod 4"

    return exp(a, (p + 1) / 4, p)


# Fonctions demandées dans le TME

# Q1


def est_elliptique(E):
    """
    Renvoie True si la courbe E est elliptique et False sinon.

    E : un triplet (p, a, b) représentant la courbe d'équation
    y^2 = x^3 + ax + b sur F_p, p > 3
    """
    p, a, b = E
    l1 = 4 * exp(a, 3, p)
    l2 = 27 * exp(b, 2, p)
    l1 = exp(l1, 1, p)
    l2 = exp(l2, 1, p)

    if (l1 + l2) % p == 0:
        return False

    return True

# Q2


def point_sur_courbe(P, E):
    """Renvoie True si le point P appartient à la courbe E et False sinon.
    """
    if P == ():
        return True

    p, a, b = E
    x, y = P
    carreY = exp(y, 2, p)
    Y = exp(x, 3, p) + a * x + b
    Y = exp(Y, 1, p)

    return carreY == Y

# Q3


def symbole_legendre(a, p):
    """Renvoie le symbole de Legendre de a mod p.
    """
    return exp(a, (p - 1) // 2, p)

# Par le théorème de Fermat + dans un anneau intègre,
# un polynôme n'a jamais plus de racines que son degré.
# f(FpX) d'ordre (p - 1) / 2 => pour tout z residu quadratique,
# ie z appartient à f(FpX), z ^ ((p - 1) / 2) mod p = 1 = (z / q)
# P(X) = X ^ (p - 1) - 1 : {x appartient a FpX | P(x) = 0} = FpX (Petit Théorème de Fermat)
# Donc P(X) = 0 <=> (X ^ (p - 1 / 2) - 1) * (X ^ (p - 1 / 2) + 1) = 0
# Fp[X] est un anneau intègre

# Q4


def cardinal(E):
    """Renvoie le cardinal du groupe de points de la courbe E.
    """
    p, a, b = E
    cardinal = 1

    for i in range(p):
        Y = (exp(i, 3, p) + a * i + b) % p
        X = symbole_legendre(Y, p)
        if X == 0:
            cardinal += 1
        if X == 1:
            cardinal += 2

    return cardinal

# Q5


def liste_points(E):
    """Renvoie la liste des points de la courbe elliptique E.
    """
    p, a, b = E

    assert p % 4 == 3, "erreur: p n'est pas congru à 3 mod 4."

    liste = [()]

    for i in range(p):
        Y = (exp(i, 3, p) + a * i + b) % p
        X = symbole_legendre(Y, p)
        if X == 0:
            liste.append((i, 0))
        if X == 1:
            s = racine_carree(Y, p)
            liste.append((i, s))
            liste.append((i, p-s))

    return liste

# Vérification :
# si p = 3 mod(4), p + 1 est divisible par 4 donc
# p + 1 / 4 est entier. Or par le petit théorème de Fermat,
# a ** p = a mod(p) donc a ** (p + 1) = a ** 2 mod(p).
# Donc en divisant la puissance par 4 on a :
# a ** (p + 1) / 4 = a ** (2 / 4) mod(p) = racine carré de a mod(p).

# Q6
# Théorème de Hasse:
# p + 1 - 2 * sqrt(p) <= E <= p + 1 + 2 * sqrt(p)


def cardinaux_courbes(p):
    """
    Renvoie la distribution des cardinaux des courbes elliptiques
    définies sur F_p.

    Renvoie un dictionnaire D où D[i] contient le nombre de courbes elliptiques
    de cardinal i sur F_p.
    """
    D = {}
    bas = int(p + 1 - 2 * sqrt(p))
    haut = int(p + 1 + 2 * sqrt(p))

    for i in range(bas + 1, haut + 1):
        D[i] = 0
    for a in range(p):
        for b in range(p):
            E = p, a, b
            Y = cardinal(E)
            if est_elliptique(E):
                D[Y] += 1

    return D


def dessine_graphe(p):
    """Dessine le graphe de répartition des cardinaux des
    courbes elliptiques définies sur F_p.
    """
    bound = int(2 * sqrt(p))
    C = [c for c in range(p + 1 - bound, p + 1 + bound + 1)]
    D = cardinaux_courbes(p)

    plt.bar(C, [D[c] for c in C], color='b')
    plt.show()

# Q7


def moins(P, p):
    """Retourne l'opposé du point P mod p.
    """
    x, y = P
    y2 = p - y

    return x, y2


def est_egal(P1, P2, p):
    """Teste l'égalité de deux points mod p.
    """
    if est_zero(P1) and est_zero(P2):
        return True
    if est_zero(P1) or est_zero(P2):
        return False

    x1, y1 = P1
    x2, y2 = P2

    return x1 % p == x2 % p and y1 % p == y2 % p


def est_zero(P):
    """Teste si un point est égal au point à l'infini.
    """
    if P == ():
        return True

    return False

# Q8


def addition(P1, P2, E):
    """Renvoie P1 + P2 sur la courbe E.
    """
    if P1 == ():
        return P2
    if P2 == ():
        return P1

    p, a, b = E
    x1, y1 = P1
    x2, y2 = P2

    if x1 % p == x2 % p and y2 % p == -y1 % p:
        return ()
    else:
        if est_egal(P1, P2, p):
            l = ((3 * exp(x1, 2, p) + a) * inv_mod(2 * y1, p)) % p
        else:
            l = ((y2 - y1) * inv_mod(x2 - x1, p)) % p
        x3 = (exp(l, 2, p) - x1 - x2) % p
        y3 = (l * (x1 - x3) - y1) % p

    return x3, y3

# Q9


def multiplication_scalaire(k, P, E):
    """Renvoie la multiplication scalaire k*P sur la courbe E.
    """
    def binaire(N):
        L = list()
        while (N > 0):
            L.append(N % 2)
            N = N // 2
        L.reverse()
        return L

    p, a, b = E
    res = ()

    for Ni in binaire(abs(k)):
        res = addition(res, res, E)
        if Ni == 1:
            res = addition(res, P, E)
    if k < 0:
        return moins(res, p)

    return res

# Q10


def ordre(N, factors_N, P, E):
    """Renvoie l'ordre du point P dans les points de la courbe E mod p.
    N est le nombre de points de E sur Fp.
    factors_N est la factorisation de N en produit de facteurs premiers.
    """
    p, a, b = E

    if P == ():
        return 1
    if est_zero(P):
        return 2

    liste = []

    for i in factors_N:
        x, y = i
        for j in range(1, y + 1):
            liste.append(x * j)
    # On ajoute tous les multiples de N à notre liste
    while(True):
        check = False
        for i in liste:
            for j in liste:
                test = i * j
                if test <= N and N % test == 0 and test not in liste:
                    check = True
                    liste.append(test)
        if not check:
            break

    x1, y1 = P

    while(len(liste) > 1):
        val = liste[randint(0, len(liste) - 1)]
        P2 = multiplication_scalaire(val, P, E)

        # Si on tombe sur l'ordre du groupe ou un de ses multiples,
        # on supprime alors toutes les valeurs supérieures à ce nombre

        if P2 == ():
            for i in liste:
                if i > val:
                    liste.remove(i)
            continue
        x2, y2 = P2
        if x1 == x2 and y1 == p - y2:
            for i in liste:
                if i > val:
                    liste.remove(i)
            continue

        # Sinon on supprime tous les multiples de val
        # (si 4 n'est pas l'ordre du groupe alors 2 non plus)

        else:
            for i in liste:
                if i < val and val % i == 0:
                    liste.remove(i)
            liste.remove(val)
            continue

    return liste[0]

# Q11


def point_aleatoire_naif(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E.
    """
    p, a, b = E
    cpt = 0

    while(True):
        cpt += 1
        x = randint(0, p - 1)
        y = randint(0, p - 1)
        if point_sur_courbe((x, y), E):
            print("Nb iterations :", cpt)
            return x, y

    return

# point_aleatoire_naif((360040014289779780338359, 117235701958358085919867, 18575864837248358617992))
# On observe que plus p est grand, plus l'algorithme prend du temps
# Pour E donné dans l'énoncé, l'algorithme est interminable
# car la probabilité de trouver un point est trop faible.
# La complexité de l'algorithme est en O(p) car on tire
# au hasard 2 nombres compris entre 0 et p - 1 compris.

# Q12


def point_aleatoire(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E.
    """
    p, a, b = E

    assert p % 4 == 3, "erreur: p n'est pas congru à 3 mod 4."

    cpt = 0

    while(True):
        cpt += 1
        x = randint(0, p - 1)
        l1 = (exp(x, 3, p) + a * x + b) % p
        y = exp(l1, (p + 1) // 4, p)
        if point_sur_courbe((x, y), E):
            print("Nb iterations :", cpt)
            return x, y

    return

# point_aleatoire((360040014289779780338359, 117235701958358085919867, 18575864837248358617992))
# On observe que le nombre d'itérations est beaucoup plus petit
# par rapport à la fonction naif.
# Pour E donné dans l'énoncé, l'algorithme itère entre
# 1 et 6 fois.
# La complexité de l'algorithme est en O(1) car on a une
# probabilité de tomber sur un carré de 0.5.

# Q13


def point_ordre(E, N, factors_N, n):
    """Renvoie un point aléatoire d'ordre N sur la courbe E.
    Ne vérifie pas que n divise N.
    """
    p, a, b = E

    while(True):
        P = point_aleatoire(E)
        x = ordre(N, factors_N, P, E)
        if x == n:
            return P

    return

# Q14


def keygen_DH(P, E, n):
    """Génère une clé publique et une clé privée pour un échange Diffie-Hellman.
    P est un point d'ordre n sur la courbe E.
    """
    p, a, b = E

    if P == ():
        return (1, 1)

    sec = n
    pub = exp(n, a, p)

    return sec, pub


def echange_DH(sec_A, pub_B, E):
    """Renvoie la clé commune à l'issue d'un échange Diffie-Hellman.
    sec_A est l'entier secret d'Alice et pub_b est l'entier public de Bob.
    """
    p, a, b = E
    K = exp(pub_B, sec_A, p)

    return K, K

# Q15
# Pour trouver un bon point P pour un échange de clé
# Diffie-Hellman, il faut chercher un ordre suffisamment
# grand par rapport au cardinal de la courbe.
# Pour cela, on appelle la fonction point_ordre() pour trouver un
# point d'ordre assez grand.


def Q15(p):
    """Renvoie un bon point pour un échange de
    clé Diffie-Hellman.
    """
    E = (p, 1, 0)
    N = 248301763022729027652019747568375012324
    factors_N = [(2, 2), (62075440755682256913004936892093753081, 1)]
    P = point_ordre(E, N, factors_N, 62075440755682256913004936892093753081)

    print("Point: ", P)

    return P

if __name__ == "__main__":
    p = 248301763022729027652019747568375012323
    Q15(p)

