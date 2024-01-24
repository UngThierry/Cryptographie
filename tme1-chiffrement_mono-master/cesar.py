#!/usr/bin/python3

# Usage: python3 cesar.py clef c/d phrase
# Returns the result without additional text

def chiff_cesar_nb(nb,cle):
    return (nb+cle)%26

def dechiff_cesar_nb(nb,cle):
    return (nb-cle)%26

def chiff_cesar(text,cle):
    text_chiffre=""
    for i in text:
       # i devient n de 0 à 25
       #Maj / min
        if ord(i) < 97:
            dn = 65
        else:
            dn = 97
        n = ord(i) - dn
        n_chiffre=chiff_cesar_nb(n,cle) # n_chiffre reçois la valeur numerique du chiffrement de la valeur numerique de i
        i_chiffre=chr(n_chiffre+dn) # retour au lettres
        text_chiffre+=i_chiffre # concaténation de la chaine chiffré avec le caractere chiffré

    return text_chiffre

def cesar_attaque(text,cle):
    return chiff_cesar(text,-cle)  # appel à cesar_chiffre avec -cle