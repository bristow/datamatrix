#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generation_datamatrix.py
#  
#  Copyright 2015 Cédric Frayssinet et Frédéric Gauthier
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

'''
''Importation des modules nécessaires
'''
from PIL import Image							# on travaille sur des images
import sys						


'''
''Déclaration des variables générales
'''

largeur_bit = 16								#nombre de pixels pour définir le bit dans le datamatrix
largeur = largeur_bit*8+2*largeur_bit			#taille du datamatrix maxi
hauteur = largeur_bit*8+2*largeur_bit			#ce sera un datamatrix carré
couleur = 'L'									#niveau de gris
couleur_fond = 'white' 							#fond blanc
tab_code = []									#liste de mes octets à encoder en datamatrix
code = Image.new(couleur, (largeur, hauteur), couleur_fond)		#création d'une image qui sera mon datamatrix
pix = code.load()								#les acces via cet objet sont plus rapide que getpixel et putpixel
message = []


'''
''Matrice de placement de tous les bits en fonction des 8 octets dans le datamatrix de 8x8 cases
''La premiere liste correspond aux coordonnées du premier octet et ainsi de suite
'''
placement_octet =  [[(6,2) , (7,2) , (6,3) , (7,3) , (0,3) , (6,4) , (7,4) , (0,4)],
					[(0,0) , (1,0) , (0,1) , (1,1) , (2,1) , (0,2) , (1,2) , (2,2)],
					[(2,6) , (3,6) , (2,7) , (3,7) , (4,7) , (2,0) , (3,0) , (4,0)],
					[(5,7) , (6,7) , (5,0) , (6,0) , (7,0) , (5,1) , (6,1) , (7,1)],
					[(3,1) , (4,1) , (3,2) , (4,2) , (5,2) , (3,3) , (4,3) , (5,3)],
					[(1,3) , (2,3) , (1,4) , (2,4) , (3,4) , (1,5) , (2,5) , (3,5)],
					[(7,5) , (0,5) , (7,6) , (0,6) , (1,6) , (7,7) , (0,7) , (1,7)],
					[(4,4) , (5,4) , (4,5) , (5,5) , (6,5) , (4,6) , (5,6) , (6,6)]]

'''
''FONCTIONS UTILISEES DANS LE PROGRAMME
'''

'''
''dessin du contour du datamatrix
''c'est normalisé, noir sur la premiere colonne et derniere ligne
''alterné sur la première ligne et la derniere colonne
'' 0 correspond à la couloir noire
'' 255 à la couleur blanche
'''
def dessin_encadrement():
	for h in range(hauteur):			#dessin de la premiere colonne (noir)
		for b in range(largeur_bit):	
			pix[b, h] = 0
	for l in range(largeur):			#dessin de la derniere ligne (noir)
		for b in range(largeur_bit):
			pix[l, hauteur-b-1] = 0
	for l in range(int(largeur/(2*largeur_bit))): 	#dessin premiere ligne (alterné)
		for b in range(largeur_bit):
			for e in range(largeur_bit):
				pix[l*2*largeur_bit+e, b] = 0
	for h in range(int(hauteur/(2*largeur_bit))):	#dessin dernière colonne (alterné)
			for b in range(largeur_bit):
				for e in range(largeur_bit):
					pix[(largeur-1)-b, (hauteur-1)-(h*2*largeur_bit+e)] = 0

'''
''Conversion d'un nombre décimal en nombre binaire de nb=8 bits
''Permet de ne pas afficher 0b en début d'octet
'''
def decimal_to_binaire(d,nb=8):
    if d == 0:
        return "0".zfill(nb)	#j'ajoute 0 sur mon mot de 8 bits
    b=""
    while d != 0:
        d, r = divmod(d, 2)		#division euclidienne
        b = "01"[r] + b
    return b.zfill(nb)			#je renvoie mon mot b écrit dans les 8 bits

'''
''Génération de la liste tab_code au format binaire ['010101001','1010101011',...]
''en fonction de la chaîne de caractères donnée par l'utilisateur (data)
'''
def encodage_donnees():
	nombre = ''	
	if len(data) > 16:
		print("Vous avez donné plus de 16 caractères, c'est sûr, cela ne rentrera pas dans ce datamatrix !")
	else:
		print("J'encode cela : {}".format(data))
	for pos,car in enumerate(data):
		if 48 <= ord(car) <= 57 and (pos != len(data)-1 or 48 <= ord(car) <= 57):
			#on rentre dans la boucle si c'est un chiffe ET (ce n'est pas le dernier ou c'est un chiffre)
			#print("j'ai un chiffre")
			nombre = nombre+car
			if len(nombre) == 2:
				#print("Je suis à 2 chiffres, j'encode, et je met nombre à vide")
				tab_code.append(decimal_to_binaire(int(nombre)+130))
				nombre = ''
			if len(nombre) == 1 and pos == len(data)-1:
				#print("Je suis le dernier chiffre à encoder")
				tab_code.append(decimal_to_binaire(ord(car)))
				nombre = ''
		else:
			if len(nombre) == 1:
				#print("j'ai un chiffre tout seul que j'encode et je met nombre à vide")
				tab_code.append(decimal_to_binaire(ord(str(nombre))))
				nombre = ''
			#print("j'ai un caractère alpha ou numérique que j'encode")
			tab_code.append(decimal_to_binaire(ord(car)))

'''
''On remplit le datamatrix avec les valeurs (octets) du tableau tab_code
'''
def remplissage_selon_octet():
	for o in range(len(tab_code)):								#parcours de mon tableau d'octet tab_code
		octet = tab_code[o]										#octet permet de connaître mon octet en cours d'écriture
		#print("On gère l'octet {} : {}".format(o+1,octet))
		for bit,coordonnees in zip(octet,placement_octet[o]):	#Zip permet d'itérer sur 2 listes, et donc obtenir le bit et les coordonnées sur les 2 listes
			X = coordonnees[0]									#on recupère la première valeur du tuple pour X
			Y = coordonnees[1]									#on recupère la première valeur du tuple pour Y
			#print("Le bit sera à {} à la coordonnée ({},{})".format(bit, X, Y))
			for e1 in range(largeur_bit):						#pour remplir sur X la largeur de bit
				for e2 in range(largeur_bit):					#pour remplir sur Y la largeur de bit
					if bit == "1":
						pix[largeur_bit+X*largeur_bit+e1,largeur_bit+Y*largeur_bit+e2] = 0	#+largeur_bit permet de ne pas écrire sur le cadre
					else:																	#on écrit en noir (couleur 0) si bit=1
						pix[largeur_bit+X*largeur_bit+e1,largeur_bit+Y*largeur_bit+e2] = 255#sinon on écrit en blanc



def lecture_image(im):
	img = Image.open(im)
	tab_code_depuis_image = []
	moitie_bit = largeur_bit / 2
	for bit,coordonnees_octet in enumerate(placement_octet):
		#print("Coordonnées (x, y) pour le bit n°{} : {}".format(bit,coordonnees_octet))
		octet = ''
		for coordonnees in coordonnees_octet:
			X = largeur_bit + coordonnees[0]*largeur_bit + moitie_bit
			Y = largeur_bit + coordonnees[1]*largeur_bit + moitie_bit
			#print("Le bit {} a la coordonnée ({},{})".format(bit, X, Y))
			pixou = img.getpixel((X, Y))
			if pixou == 255:	#si on trouve la couleur blanche 255, on met le bit à 0 !
				pixou = 0
			else:
				pixou = 1
			octet = octet+str(pixou)
		tab_code_depuis_image.append(octet)
	return(tab_code_depuis_image)


def decodage_depuis_tab_code(tab):
	for octet in tab_code:
		decimal = int(octet,2)
		print("Décodage de l'octet {}, qui donne en décimal : {}".format(octet,decimal))
		if 48 <= decimal <= 57:
			carac = chr(decimal)
			print("C'est un chiffre seul : {}".format(carac))
		if decimal > 130:
			carac = str(decimal - 130)
			print("C'est une doublette de chiffres : {}".format(carac))
		if decimal == 130:
			print("C'est un double zéro")
			carac = '00'
		if 32 <= decimal <= 47 or 58 <= decimal < 130:
			carac = chr(decimal)
			print("C'est un caractère alpha : {}".format(carac))
		message.append(carac)

	message_encode = "".join(message)
	return(message_encode)

'''
''PROGRAMME PRINCIPAL
'''

#Demander au joueur une lettre ou un mot.
data = input("Que souhaitez-vous encoder (encodage sur 8 octets maximum) ? ")
try:
	encodage_donnees()
	nb_octets = len(tab_code)
	if nb_octets == 8:
		print("Parfait, nous avons {} octets à encoder, voici le DataMatrix qui s'affiche.".format(nb_octets))
	if nb_octets < 8:
		print("Nous avons {} octets à encoder, voici le DataMatrix correspondant, il est forcément incomplet.".format(nb_octets))
	dessin_encadrement()
	remplissage_selon_octet()
	print(tab_code)
	#Affichage de l'image dans une fenêtre
	code.show()
	#Sauvegarde de l'image au format PNG
	code.save('DataMatrix_{}x{}_{}pix_{}.png'.format(largeur, hauteur, largeur_bit, data))
	#confirmation de la bonne sauvegarde
	print("Le DataMatrix est sauvegardé sous le nom : DataMatrix_{}x{}_{}pix_{}.png.".format(largeur, hauteur, largeur_bit, data))
	
	#on vérifie l'image pour décoder la chaine de départ
	#on envoie le fichier image généré dans la fonction lecture_image()
	#puis on lance le décodage avec la fonction decodage_depuis_tab_code()
	#on stocke le return dans message_encode pour l'afficher juste après
	message_encode = decodage_depuis_tab_code(lecture_image('DataMatrix_{}x{}_{}pix_{}.png'.format(largeur, hauteur, largeur_bit, data)))	#tab_code renvoyé par la fonction lecture_image
	
	print("Voici la chaîne de caractères encodées dans ce DataMatrix : {}".format(message_encode))

except IndexError:
	#if nb_octets > 8:
	print("L'encodage dépasse 8 octets, merci de réduire les données à encoder !")
	sys.exit()
	


