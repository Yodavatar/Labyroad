#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad

import os

class Donnee():
    def __init__(self,screen):
        """Get the data of the game"""
        self.taille_text = int(screen.get_width() * 50 /1920)
        self.moyen_text = int(self.taille_text/1.5)
        self.mini_text = int(self.taille_text/2)
        #zoom ecran
        self.zoom = screen.get_width()*3/1280
        #Succes
        self.victoire_easy = int
        self.victoire_normal = int
        self.victoire_difficile = int
        #defaite
        self.defaite_easy = int
        self.defaite_normal = int
        self.defaite_difficile = int

    def coupe_virg(self,chaine):
        """decoupe une chaine de caractère en 2 à la virgule"""
        statu = True
        chaine1 = ""
        chaine2 = ""
        for l in chaine:
            if l == ",":
                statu = False
            elif statu:
                chaine1 += l
            else:
                chaine2 += l
        return((int(chaine1),int(chaine2)))

    def recuperer(self):
        """recupere les données des succes"""
        fichier = open("data/succes.txt","r")
        nbr = 0
        for line in fichier:
            nbr += 1
            if nbr == 1:
                self.victoire_easy,self.defaite_easy = self.coupe_virg(line[0:-1])
            elif nbr == 2:
                self.victoire_normal,self.defaite_normal = self.coupe_virg(line[0:-1])
            elif nbr == 3:
                self.victoire_difficile,self.defaite_difficile = self.coupe_virg(line[0:-1])

    def sauvegarder(self):
        """enregister les succes dans un fichier
        les données enregistées sont les victoires des differents mode de jeu"""
        fichier = open("data/succes.txt","w")
        fichier.write(str(self.victoire_easy)+","+str(self.defaite_easy)+"\n")
        fichier.write(str(self.victoire_normal)+","+str(self.defaite_normal)+"\n")
        fichier.write(str(self.victoire_difficile)+","+str(self.defaite_difficile)+"\n")
        fichier.close()

    def delete(self):
        """Suprime les succes"""
        os.remove("data/succes.txt")
        fichier = open("data/succes.txt","w")
        fichier.write("0,0\n")
        fichier.write("0,0\n")
        fichier.write("0,0\n")
        fichier.close()

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad