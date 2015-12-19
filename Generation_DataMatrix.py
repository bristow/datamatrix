#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generation_datamatrix.py
#  
#  Copyright 2015 Bristow
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
placement_octet = [[(6,2) , (7,2) , (6,3) , (7,3) , (0,3) , (6,4) , (7,4) , (0,4)],[(0,0) , (1,0) , (0,1) , (1,1) , (2,1) , (0,2) , (1,2) , (2,2)],[(2,6) , (3,6) , (2,7) , (3,7) , (4,7) , (2,0) , (3,0) , (4,0)],[(5,7) , (6,7) , (5,0) , (6,0) , (7,0) , (5,1) , (6,1) , (7,1)],[(3,1) , (4,1) , (3,2) , (4,2) , (5,2) , (3,3) , (4,3) , (5,3)],[(1,3) , (2,3) , (1,4) , (2,4) , (3,4) , (1,5) , (2,5) , (3,5)],[(7,5) , (0,5) , (7,6) , (0,6) , (1,6) , (7,7) , (0,7) , (1,7)],[(4,4) , (5,4) , (4,5) , (5,5) , (6,5) , (4,6) , (5,6) , (6,6)]]



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
''Génération aléatoire rempli de 0 et de 255 d'un tableau aux dimensions données ci-dessus
'''
def generation_tableau_aleatoire():
	global tab_code
	for h in range(int(hauteur/largeur_bit)):
		tab_i = []
		for i in range(int(largeur/largeur_bit)):
			if randint(0,100) <= 50:
				tab_i.append(0)
			else:
				tab_i.append(255)
		tab_code.append(tab_i)


'''
''dessin du datamatrix à l'aide du tableau de valeurs tab_code
''La longueur du tableau est la largeur / largeur bit, soit 36 si 288/8

def dessin_datamatrix():
	for h in range(1,len(tab_code)-1):					#le 1 et -1 permet de supprimer le cadre haut et bas du datamatrix
		for i,j in enumerate(tab_code[h]):				#enumerate renvoie en i l'index, et en j la valeur 0 ou 255
			for e in range(largeur_bit):				#pour remplir sur X la largeur de bit
				for k in range(largeur_bit):			#pour remplir sur Y la largeur de bit
					if i != 0 and i != len(tab_code)-1: #permet de supprimer le cadre gauche et droite du datamatrix
						pix[i*largeur_bit+e, h*largeur_bit+k] = j
'''


def remplissage_selon_octet(octet):
	for h in range(len(placement_octet)):
		for i,coordonnees in enumerate(placement_octet[h]):
			for e in range(largeur_bit):				#pour remplir sur X la largeur de bit
				for k in range(largeur_bit):			#pour remplir sur Y la largeur de bit
					if i != 0 and i != len(tab_code)-1: #permet de supprimer le cadre gauche et droite du datamatrix
						X = coordonnees[0]
						Y = coordonnees[1]
						bit = octet[i]
						pix[largeur_bit+X*largeur_bit+e,largeur_bit+Y*largeur_bit+k] = bit


#Appel des fonctions
dessin_encadrement()
generation_tableau_aleatoire()

for h in range(len(tab_code)):
	remplissage_selon_octet(tab_code[h])
	
#Affichage de l'image dans une fenêtre
code.show()

#Sauvegarde de l'image au format PNG
code.save('DataMatrix_{}x{}_{}pix.png'.format(largeur, hauteur, largeur_bit))

