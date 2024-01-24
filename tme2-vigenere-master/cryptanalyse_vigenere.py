# Sorbonne Université 3I024 2018-2019
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : UNG 3804472
# Etudiant.e 2 : NOM ET NUMERO D'ETUDIANT

import sys, getopt, string, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français
# À modifier
freq_FR = [0.09213414037491088,  0.010354463742221126,  0.030178915678726964,  0.03753683726285317,  0.17174710607479665,  0.010939030914707838,  0.01061497737343803,  0.010717912027723734,  0.07507240372750529,  0.003832727374391129,  6.989390105819367e-05,  0.061368115927295096,  0.026498684088462805,  0.07030818127173859,  0.049140495636714375,  0.023697844853330825,  0.010160031617459242,  0.06609294363882899,  0.07816806814528274,  0.07374314880919855,  0.06356151362232132,  0.01645048271269667,  1.14371838095226e-05,  0.004071637436190045,  0.0023001447439151006,  0.0012263202640210343]

# Chiffrement César
def chiffre_cesar(txt, key):
    """
    Parcours le texte par lettre et renvoit un texte 
    chiffré avec key décalage
    @param txt, key
    @return text chiffré
    """
    message_chiffre = ""
    for i in txt:
        message_chiffre += alphabet[(alphabet.index(i)+key)%26]
    txt = message_chiffre
    return txt

# Déchiffrement César
def dechiffre_cesar(txt, key):
    """
    Parcours le texte par lettre et renvoit un texte 
    déchiffré avec key décalage
    @param txt, key
    @return text déchiffré
    """
    message_dechiffre = ""
    for i in txt:
        message_dechiffre += alphabet[(alphabet.index(i)-key)%26]
    txt = message_dechiffre
    return txt

# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """
    Parcours le texte par lettre et renvoit un texte 
    chiffré avec la clé correspondante dans key
    @param txt, key
    @return text chiffré
    """
    message_chiffre = ""
    for i in range(len(txt)):
	    message_chiffre += alphabet[(alphabet.index(txt[i])+key[i%len(key)])%26]
    return message_chiffre

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """
    Parcours le texte par lettre et renvoit un texte 
    déchiffré avec la clé correspondante dans key
    @param txt, key
    @return text déchiffré
    """
    message_dechiffre = ""
    for i in range(len(txt)):
        message_dechiffre += alphabet[(alphabet.index(txt[i])-key[i%len(key)])%26]
    return message_dechiffre

# Analyse de fréquences
def freq(txt):
    """
    Parcours l'alphabet, si la lettre se trouve dans le texte, on l'ajoute à hist
    @param txt
    @return hist #tableau de fréquence
    """
    hist = []
    for i in alphabet:	
	    hist.append(txt.count(i))
    return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Retourne l'indice dans l'alphabet de la lettre la plus fréquente d'un texte
    @param text
    @return indice de la lettre la plus fréquente
    """
    return freq(txt).index(max(freq(txt)))

# indice de coïncidence
def indice_coincidence(hist):
    """
    Retourne la somme de fréquence de chaque lettre sur la longueur d'un texte
    @param hist #tableau de fréquence
    @return indice de coïncidence
    """
    somme = 0
    if(sum(hist)>1):
        for i in hist:
            somme += (i*(i-1))/((sum(hist)*(sum(hist)-1)))
    return somme

# Recherche la longueur de la clé
def longueur_clef(cipher):
    """
    Parcours deux boucles imbriquées, ajoute les indices de coïncidences
    de chaque colonnes dans un tableau. Puis fait la moyenne du
    tableau et renvoit l'indice de la premiere occurence de valeur > 0.06
    @param cipher
    @return longueur 
    """
    list = []
    ic = []
    for i in range(1,21):
	    for j in range(0,i):
		    list = cipher[j::i]
		    f = freq(list)
		    ic.append(indice_coincidence(f))
	    moy = sum(ic)/len(ic)
	    ic.clear()
	    if moy > 0.06:
		    return i
    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Réordonne le texte en colonnes allant de 0 à key_length(colonnes) 
    Cherche la lettre la plus fréquente à chaque fois puis
    soustrait l'indice de la lettre la plus fréquente en alphabet
    @param key_length
    @return décalages #tableau de décalage pour lettre de la clé
    """
    decalages = [0]*key_length
    for i in range(0,key_length):
	    list = cipher[i::key_length]
	    a = lettre_freq_max(list)
	    clef = ((22-(26-a))+26)%26   #22 correspond a 26-index('E')
	    decalages[i] = clef
    return decalages

# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Retourne le texte dechiffré
    @param cipher
    @return decipher
    """
    return dechiffre_vigenere(cipher,clef_par_decalages(cipher,longueur_clef(cipher)))

# CryptAnalyse V1:
# On a 18 textes correctement déchiffrés.
# Les textes qui échouent sont les textes courts.
# Donc les textes ne sont pas assez long alors les colonnes produit lors de calcul
# d'indice mutuel sont courts pour une analyse fréquentielle, donc ça fournit moins
# d'information sur les décalages.

################################################################

### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
    Retourne l'indice de coïncidence mutuelle de h1 et h2, décallé
    de d
    @param h1, h2, d #(h1, h2) fréquence de lettre de deux textes
    @return indice de coïncidence mutuelle
    """
    res = 0.0
    total = sum(h1)*sum(h2)
    h2 = h2[d:]+h2[:d]
    for i in range(0,26):
	    res += (h1[i]*h2[i])/total
    return res

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Renvoie le tableau des décalages probables étant donné la longueur 
    de la clé en comparant l'indice de décalage mutuel par rapport
    à la première colonne
    @param cipher, key_length
    @return tableau de décalage probables 
    """
    decalages = [0]*key_length
    icm_tab = []
    colonne_1 = freq(cipher[0:len(cipher):key_length])
    for i in range(key_length):
        colonne_i = freq(cipher[i:len(cipher):key_length])
        for j in range(0,len(alphabet)):
            icm = indice_coincidence_mutuelle(colonne_1,colonne_i,j)
            icm_tab.append(icm)
        decalages[i] = icm_tab.index(max(icm_tab))
        icm_tab = []           
    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Retourne le texte déchiffré 
    @param cipher
    @return decipher
    """
    key_length = longueur_clef(cipher)
    deca = tableau_decalages_ICM(cipher,key_length)
    text_cesar = dechiffre_vigenere(cipher,deca)
    text_clair = ""
    freq_max = lettre_freq_max(text_cesar)
    mon_decalage = (freq_FR.index(max(freq_FR))-freq_max)%26
    text_clair = chiffre_cesar(text_cesar,mon_decalage)
    return text_clair

# CryptAnalyse V2:
# On a 43 textes correctement déchiffrés.
# Les textes qui échouent sont les textes avec une longueur de clé assez grande pour des textes courts.
# Donc le nombre de textes déchiffrés augmente, car on a changé la méthode de cryptanalyse frequentielle
# par une cryptanalyse avec l'indice de coïncidence mutuel. Toutefois le nombre des textes qui échouent
# est toujours supérieur à 50 % car d'un point de vue théorique, la méthode de ICM nécessite une taille de
# texte assez longue pour pouvoir négliger l'erreur.

################################################################

### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1,L2):
    """
    Returne la corrélation entre ces 2 listes
    @param L1, L2
    @return corrélation 
    """
    esperanceL1 = sum(L1)/len(L1)
    esperanceL2 = sum(L2)/len(L2)
    res = 0.0
    resX = 0.0
    resY = 0.0
    for i in range(len(L1)):
        resX += (L1[i]-esperanceL1)**2
        resY += (L2[i]-esperanceL2)**2
        res += (L1[i]-esperanceL1)*(L2[i]-esperanceL2)
    resX = math.sqrt(resX*resY)
    return res/resX

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Retourne la moyenne des corrélations maximales entre freq_FR et i-eme colonne (i allant
    de 0 à key_length)
    @param cipher, key_length
    @return moyenne des corrélations maximales, clef 
    """
    key = []
    cor_max = []
    score = 0.0
    i = 0
    while(i<key_length):
        l = []
        for j in range(26):
            l.append(correlation(freq_FR,freq(dechiffre_cesar(cipher[i::key_length],j))))
        cor_max.append(max(l))
        key.append(l.index(max(l)))
        i += 1
    score = sum(cor_max)/key_length
    return (score,key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Retourne le texte dechiffré
    @param cipher
    @return decipher
    """
    key_length = longueur_clef(cipher)
    score, key = clef_correlations(cipher,key_length)
    text = dechiffre_vigenere(cipher,key)
    return text

# CryptAnalyse V3:
# On a 84 textes correctement déchiffrés.
# Les textes qui échouent sont les textes un peu trop courts pour une analyse correcte.
# Donc notre cryptanalyse n'est pas rentable lorsque le texte est court et la clef
# très longue donc le rapport de corrélation n'est pas significatif pour ces exemples.

################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################

# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])