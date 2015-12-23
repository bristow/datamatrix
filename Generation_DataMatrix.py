#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generation_datamatrix.py
#  
#  Copyright 2015 XXXX
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
from PIL import Image
from random import *

'''
''Déclaration des variables
'''

largeur_bit = 8									#nombre de pixel pour définir le bit dans le datamatrix
largeur = largeur_bit*8+2*largeur_bit			#taille du datamatrix maxi
hauteur = largeur_bit*8+2*largeur_bit			#ce sera un datamatrix carré
couleur = 'L'									#niveau de gris
couleur_fond = 'white' 							#fond blanc
tab_code = []
code = Image.new(couleur, (largeur, hauteur), couleur_fond)
pix = code.load()


'''
''Matrice de placement de tous les bits en fonction des 8 octets dans le datamatrix
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
''dessin du contour du datamatrix
'' 0 correspond à la couloir noire
'' 255 à la couleur blanche
'''
def dessin_encadrement():
	for h in range(hauteur):			#dessin du bord plein gauche vertical
		for b in range(largeur_bit):	
			pix[b, h] = 0
	for l in range(largeur):			#dessin du bord plein bas horizontal
		for b in range(largeur_bit):
			pix[l, hauteur-b-1] = 0
	for l in range(int(largeur/(2*largeur_bit))): 	#dessin du bord alterné haut horizontal
		for b in range(largeur_bit):
			for e in range(largeur_bit):
				pix[l*2*largeur_bit+e, b] = 0
	for h in range(int(hauteur/(2*largeur_bit))):	#dessin du bord alterné droite vertical
			for b in range(largeur_bit):
				for e in range(largeur_bit):
					pix[(largeur-1)-b, (hauteur-1)-(h*2*largeur_bit+e)] = 0

'''
''Conversion d'un nombre décimal en nombre binaire de nb=8 bits
'''
def decimal_to_binaire(d,nb=8):
    if d == 0:
        return "0".zfill(nb)
    b=""
    while d != 0:
        d, r = divmod(d, 2)
        b = "01"[r] + b
    return b.zfill(nb)

'''
''Génération d'une liste d'octet au format binaire ['010101001','1010101011',...] de nos datas
'''
def encodage_donnees():	
	i = 0	
	while i <= len(data)-1:				#data est la chaine de caractère donnée par l'utilisateur
		couple = data[i:i+2]			#on fait des paquets de 2 chiffres
		print("Mon nombre à encoder : {}".format(couple))
		#on récupère les chiffres 2 par 2, on les colle et on ajoute 130 que l'on transforme en nombre binaire
		if len(couple) == 2:			#c'est différent si j'ai un nombre ou un chiffre
			decimal = int(couple) + 130			#[2:0] permet de supprimer le 0b du nombre binaire obtenu
			nb_bin = decimal_to_binaire(decimal)
			print("Selon la norme, j'ajoute 130 pour obtenir {} :".format(decimal))
		else:
			decimal = int(couple)
			nb_bin = decimal_to_binaire(decimal)
			print("Selon la norme, je prends le nombre tel quel {} :".format(decimal))
		tab_code.append(nb_bin)
		print("Son équivalent en binaire : {}".format(nb_bin))
		i = i+2							#permet de faire des paquets de 2 chiffres

'''
''On remplit le datamatrix avec les valeurs (octets) du tableau tab_code
'''
def remplissage_selon_octet():
	for o in range(len(tab_code)):								#parcours de mon tableau d'octet tab_code
		octet = tab_code[o]										#octet permet de connaître mon octet en cours d'écriture
		print("On gère l'octet {} : {}".format(o+1,octet))
		for bit,coordonnees in zip(octet,placement_octet[o]):	#Zip permet d'itérer sur 2 listes, et donc obtenir le bit et les coordonnées sur les 2 listes
			X = coordonnees[0]									#on recupère la première valeur du tuple pour X
			Y = coordonnees[1]									#on recupère la première valeur du tuple pour Y
			print("Le bit sera à {} à la coordonnée ({},{})".format(bit, X, Y))
			for e1 in range(largeur_bit):						#pour remplir sur X la largeur de bit
				for e2 in range(largeur_bit):					#pour remplir sur Y la largeur de bit
					if bit == "1":
						pix[largeur_bit+X*largeur_bit+e1,largeur_bit+Y*largeur_bit+e2] = 0	#+largeur_bit permet de ne pas écrire sur le cadre
					else:																	#on écrit en noir (couleur 0) si bit=1
						pix[largeur_bit+X*largeur_bit+e1,largeur_bit+Y*largeur_bit+e2] = 255

#Demander au joueur une lettre ou un mot.
data = input("Que souhaitez-vous encoder (16 chiffres maxi.) ?")

if len(data) > 16:
	print("Vous avez donné plus de 16 chiffres !")
else:
	encodage_donnees()
	dessin_encadrement()
	print(tab_code)
	remplissage_selon_octet()

	
#Affichage de l'image dans une fenêtre
print(tab_code)
code.show()

#Sauvegarde de l'image au format PNG
code.save('DataMatrix_{}x{}_{}pix.png'.format(largeur, hauteur, largeur_bit))

