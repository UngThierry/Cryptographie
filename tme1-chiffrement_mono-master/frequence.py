#!/usr/bin/python3

# Usage: python3 frequence.py(fichier_texte)

def frequence(file_name):
	text_file = None
	#Si le fichier existe on l'ouvre et on continue sinon c'est fini
	try:
		text_file = open(file_name, 'r')
	except IOError:
		print ('Entrez un nom de fichier valide')

	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	Occurences = {}
	length = 0

	for line in text_file:
		for ch in line:
			#if ch != ' ' and ch != '\n':
			length+=1
			if not (ch in Occurences):
				Occurences.update({ch: 1})
			else :
				Occurences[ch] += 1

# Print the frequences
	for c in alphabet:
		if c in Occurences:
			print (c, Occurences[c] / length)
		else:
			print (c, 0.0)

text = "germinal.txt"
print("La fréquence du texte", text, " est :")
frequence(text)

#text = "textes/text_fr"
#print("La fréquence du texte", text, " est :")
#frequence(text)

#text = "textes/text_eng"
#print("La fréquence du texte", text, " est :")
#frequence(text)