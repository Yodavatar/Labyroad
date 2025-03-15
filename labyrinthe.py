#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad

import random

class Case():
    def __init__(self) -> None:
        """Case simple possedant 4 murs pleins"""
        self.liste = [1,1,1,1]

    def change_value(self,direction=int,value=bool) -> None:
        """Fonction permettant de changer de valeur un mur de la case"""
        if value:
            self.liste[direction] = 1
        else:
            self.liste[direction] = 0

    def nbr_wall(self) -> int:
        """Renvoie le nombre de mur d'une case"""
        return(self.liste[0]+self.liste[1]+self.liste[2]+self.liste[3])

    def values(self) -> list:
        """Renvoie les valeurs des 4 murs dans une liste"""
        return([self.liste[0],self.liste[1],self.liste[2],self.liste[3]])

    def __str__(self) -> str:
        """Renvoie les valeurs des 4 murs dans une chaine de caractère"""
        return(str(self.liste[0])+str(self.liste[1])+str(self.liste[2])+str(self.liste[3]))

class Labyrinthe():
    def __init__(self,x,y) -> None:
        """Creation d'un labyrinthe de longueur x et largeur y
        le labyrinthe est constitué de x*y case de la class Case()"""
        assert x < 1000 and y < 1000,"X et Y sont trop grand"
        self.x = x-1
        self.y = y-1

        self.laby = []

        for i in range(y):
            self.laby.append([])
            for j in range(x):
                self.laby[i].append([])
                self.laby[i][j] = Case()

    def recup_val(self,x,y) -> int:
        """Recupere les valeurs d'une case du labyrinthe"""
        return(self.laby[y][x].values())

    def bordure_laby(self,x:int,y:int) -> list:
        """Renvoie une liste de direction, si
        la case touche une bordure du labyrinthe"""
        impossible = []
        if x == 0: #Touche à gauche
            impossible.append(3)
        if y == 0: #Touche en haut
            impossible.append(0)
        if x == self.x: #Touche à droite
            impossible.append(1)
        if y == self.y: #Touche en bas
            impossible.append(2)
        return impossible

    def case_ouverte(self,x:int,y:int) -> bool:
        """Renvoie si la case est ouverte ou non"""
        if 0 in self.laby[y][x].values():
            return True
        return False

    def mur_adjacent(self,x:int,y:int) -> list:
        """Renvoie une liste de direction, si
        les murs autours de la case en question existent"""
        possible = [0,1,2,3]
        murs = []
        for i in self.bordure_laby(x,y):
            possible.remove(i)
        for i in possible:
            if i == 0 and self.case_ouverte(x,y-1)==False:
                murs.append(0)
            if i == 1 and self.case_ouverte(x+1,y)==False:
                murs.append(1)
            if i == 2 and self.case_ouverte(x,y+1)==False:
                murs.append(2)
            if i == 3 and self.case_ouverte(x-1,y)==False:
                murs.append(3)
        return murs

    def passage_adjacent(self,x:int,y:int) -> list:
        """Renvoie une liste de direction, s'il existe un
        passage autours de la case en question"""
        possible = [0,1,2,3]
        passage = []
        for i in self.bordure_laby(x,y):
            possible.remove(i)
        for i in possible:
            if i == 0 and self.laby[y][x].values()[0]==0:
                passage.append(0)
            if i == 1 and self.laby[y][x].values()[1]==0:
                passage.append(1)
            if i == 2 and self.laby[y][x].values()[2]==0:
                passage.append(2)
            if i == 3 and self.laby[y][x].values()[3]==0:
                passage.append(3)
        return passage

    def retire_mur(self,x:int,y:int,direction:int) -> None:
        """Retire un mur à partir des coordonnées"""
        self.laby[y][x].change_value(direction,False)
        #nord,est,sud,ouest
        if direction == 0:
            self.laby[y-1][x].change_value(2,False)
        elif direction == 1:
            self.laby[y][x+1].change_value(3,False)
        elif direction == 2:
            self.laby[y+1][x].change_value(0,False)
        elif direction == 3:
            self.laby[y][x-1].change_value(1,False)

    def ajoute_mur(self,x:int,y:int,direction:int) -> None:
        """Ajoute un mur à partir des coordonnées"""
        self.laby[y][x].change_value(direction,True)
        #nord,est,sud,ouest
        if direction == 0:
            self.laby[y-1][x].change_value(2,True)
        elif direction == 1:
            self.laby[y][x+1].change_value(3,True)
        elif direction == 2:
            self.laby[y+1][x].change_value(0,True)
        elif direction == 3:
            self.laby[y][x-1].change_value(1,True)

    def retire_mur_aleatoire(self,x:int,y:int) -> int:
        """Retire un mur aleatoirement de la case en question
        qui donne accès à une case non ouverte et renvoie sa direction,
        si aucun mur ne peut etre enlevé, on renvoie None"""
        liste = self.mur_adjacent(x,y)
        if len(liste) == 0:
            return None
        random.shuffle(liste)
        if liste[0] == 0:
            self.retire_mur(x,y,0)
            return 0
        elif liste[0] == 1:
            self.retire_mur(x,y,1)
            return 1
        elif liste[0] == 2:
            self.retire_mur(x,y,2)
            return 2
        elif liste[0] == 3:
            self.retire_mur(x,y,3)
            return 3

    def __str__(self) -> str:
        """Renvoie le labyrinthe sous forme de texte"""
        n = []
        e = []
        s = []
        o = []
        for i in self.laby:
            for j in i:
                n.append(str(j)[0])
                e.append(str(j)[1])
                s.append(str(j)[2])
                o.append(str(j)[3])
        all = " "
        for i in range(self.x+1):#première ligne
            if n[i] == "1":
                all += "+-"
            else:
                all += "+ "
        all += "+\n"
        demi = " "
        for i in range((self.y+1)*(self.x+1)):#autres lignes
            if i % (self.x+1) == 0:# 1ere case de chaque ligne
                if o[i] == "1":
                    all += " |"
                else:
                    all += "  "
            all += " "
            if e[i] == "1":
                all += "|"
            else:
                all += " "
            if s[i] == "1":
                demi += "+-"
            else:
                demi += "+ "
            if i % (self.x+1) == self.x:# derniere case de chaque ligne
                all += "\n"+demi+"+\n"
                demi = " "
        return all

def parfait(laby:Labyrinthe):
    """Transforme le labyrinthe pour qu'il devienne
    parfait en utilisant une fontion récursive"""
    recursif_parfait(random.randint(0,laby.x),random.randint(0,laby.y),laby,[])

def recursif_parfait(x:int,y:int,laby,visite) -> None:
    """-si la case considérée est déja visitée, on ne fait rien
    -sinon on la note comme visitée et on appelle récursivement
    sur chacun de ses voisins non visités après avoir ouvert le mur avec le voisin"""
    if ((laby.x+1)*(laby.y+1)) != len(visite):
        if [x,y] not in visite:
            visite.append([x,y])#on bloque la case pour ne pas revenir dessus
            possible = laby.mur_adjacent(x,y)#on recupère les murs autours de la case
            if len(possible) == 0:
                return
            mur_direction = laby.retire_mur_aleatoire(x,y)#on enlève un mur aléatoiremant de la case
            if 0 == mur_direction:
                recursif_parfait(x,y-1,laby,visite)
            elif 1 == mur_direction:
                recursif_parfait(x+1,y,laby,visite)
            elif 2 == mur_direction:
                recursif_parfait(x,y+1,laby,visite)
            elif 3 == mur_direction:
                recursif_parfait(x-1,y,laby,visite)
            possible.remove(mur_direction)
            random.shuffle(possible)
            for i in possible:
                if 0 == i and laby.case_ouverte(x,y-1)==False:
                    laby.retire_mur(x,y,0)
                    recursif_parfait(x,y-1,laby,visite)
                if 1 == i and laby.case_ouverte(x+1,y)==False:
                    laby.retire_mur(x,y,1)
                    recursif_parfait(x+1,y,laby,visite)
                if 2 == i and laby.case_ouverte(x,y+1)==False:
                    laby.retire_mur(x,y,2)
                    recursif_parfait(x,y+1,laby,visite)
                if 3 == i and laby.case_ouverte(x-1,y)==False:
                    laby.retire_mur(x,y,3)
                    recursif_parfait(x-1,y,laby,visite)

def creer_sortie(laby:Labyrinthe) -> int:
    """Cette fonction créer une sortie dans un coin aleatoirement
    et renvoie la sortie"""
    #0=Nord Ouest/1=Nord Est/2=Sud Est/3=Sud Ouest
    nbr =(random.randint(0,3))
    if nbr == 0:#0 = Nord Ouest
        laby.laby[0][0].liste[3] = 0
        return(0)
    if nbr == 1:#1 = Nord Est
        laby.laby[0][laby.x].liste[0] = 0
        return(1)
    if nbr == 2:
        laby.laby[laby.y][laby.x].liste[1] = 0
        return(2)
    if nbr == 3:
        laby.laby[laby.y][0].liste[2] = 0
        return(3)

def trouver_sortie(laby:Labyrinthe,out=True) -> int:
    """Renvoie la position de la sortie, (y,x)
    "out" = True renvoie la position de la sortie
    à l'exterieur du labyrinthe"""
    #0=Nord Ouest/1=Nord Est/2=Sud Est/3=Sud Ouest
    if laby.laby[0][0].values()[3] == 0:
        if out:
            return (0,-1)
        else:
            return (0,0)
    if laby.laby[0][laby.x].values()[0] == 0:
        if out:
            return (-1,laby.x)
        else:
            return (0,laby.x)
    if laby.laby[laby.y][laby.x].values()[1] == 0:
        if out:
            return (laby.y,laby.x+1)
        else:
            return(laby.y,laby.x)
    if laby.laby[laby.y][0].values()[2] == 0:
        if out:
            return (laby.y+1,0)
        else:
            return(laby.y,0)
    return None

def tuto()->Labyrinthe:
    """Renvoie le labyrinthe du tuto"""
    laby = Labyrinthe(2,2)
    laby.retire_mur(0,0,2)
    laby.retire_mur(1,0,2)
    laby.retire_mur(0,0,1)
    laby.laby[1][0].liste[2] = 0
    return laby

def pos_player(laby) -> tuple:
    """renvoie la position du joueur au debut d'une manche"""
    s = trouver_sortie(laby,out=False)
    if s == (0,0):#nord ouest
        return(int((laby.y+1)*9/10),int((laby.x+1)*9/10))
    elif s == (0,laby.x):#nord est
        return(int((laby.y+1)*9/10),0)
    elif s == (laby.y,laby.x):#sud est
        return(0,0)
    elif s == (laby.y,0):#sud ouest
        return(0,int((laby.x+1)*9/10))

def resolution(laby:Labyrinthe,objectif=(0,0)):
    """Renvoie la liste des positions de la sortie jusqu'au joueur"""
    ###NE FONCTIONNE PAS###
    y,x = trouver_sortie(laby,out=False)
    recursif_resolution(laby=laby,case=[y,x],objectif=objectif,chemin=[[y,x]])

def recursif_resolution(laby:Labyrinthe,case,objectif,chemin=[]) ->list:
    """fonction recursive qui renvoie le chemin"""
    ###NE FONCTIONNE PAS###
    path_next = chemin.copy()
    possible = laby.passage_adjacent(case[0],case[1])
    if case == objectif:
        return chemin
    print(case,path_next)
    for i in possible:
        if i == 0 and [case[0]-1,case[1]] not in chemin:
            path = path_next.copy()
            path.append([case[0]-1,case[1]])
            return recursif_resolution(laby=laby,case=[case[0]-1,case[1]],objectif=objectif,chemin=path)
        if i == 1 and [case[0],case[1]+1] not in chemin:
            path = path_next.copy()
            path.append([case[0],case[1]+1])
            return recursif_resolution(laby=laby,case=[case[0],case[1]+1],objectif=objectif,chemin=path)
        if i == 2 and [case[0]+1,case[1]] not in chemin:
            path = path_next.copy()
            path.append([case[0]+1,case[1]])
            return recursif_resolution(laby=laby,case=[case[0]+1,case[1]],objectif=objectif,chemin=path)
        if i == 3 and [case[0],case[1]-1] not in chemin:
            path = path_next.copy()
            path.append([case[0],case[1]-1])
            return recursif_resolution(laby=laby,case=[case[0],case[1]-1],objectif=objectif,chemin=path)
    return None

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad