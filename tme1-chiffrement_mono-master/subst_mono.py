#!/usr/bin/python3

# Usage: python3 subst_mono.py clef c/d phrase
# Returns the result without additional text

def chiff_monoalphabetique(text,cle):
    #la cle de codage est un alphabet de la meme taille que l,alphabet d'entree dans notre cas
    #la cle de chifferement est un ensemble de lettre
    text_chiffre=''

    for i in text:
        #Maj / min
        if ord(i) < 97:
            i_chif=ord(i)-65
        else:
            i_chif = ord(i) - 97
        text_chiffre+=str(cle[i_chif])

    return text_chiffre

def dechiff_monoalphabetique(text_chiffre,cle):
    #cle de dechifferement est un ensemble de de lettres (26 dans notre cas)
    #c'est la meme cle utilisee pour chiffrer
    text=''

    for i_chif in text_chiffre:
        #si cest une majuscule ou une miniscule
        if ord(i_chif) < 97:
            dn = 65
        else:
            dn = 97

        for elem in range(26):
            if i_chif == cle[elem]:
                text += str(chr(elem + dn))

    return text