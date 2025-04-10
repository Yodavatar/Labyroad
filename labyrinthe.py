#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad

import random

class Case():
    def __init__(self) -> None:
        """The case have 4 walls"""
        self.liste = [1,1,1,1]

    def change_value(self,direction=int,value=bool) -> None:
        """Function for change the value of the wall of the case"""
        if value:
            self.liste[direction] = 1
        else:
            self.liste[direction] = 0

    def nbr_wall(self) -> int:
        """Return the number of walls"""
        return(self.liste[0]+self.liste[1]+self.liste[2]+self.liste[3])

    def values(self) -> list:
        """Return the values of the four walls"""
        return([self.liste[0],self.liste[1],self.liste[2],self.liste[3]])

    def __str__(self) -> str:
        """Return the values of the four walls in a character string"""
        return(str(self.liste[0])+str(self.liste[1])+str(self.liste[2])+str(self.liste[3]))

class Labyrinthe():
    def __init__(self,x,y) -> None:
        """Create a labyrinth of x size and y size."""
        assert x < 1000 and y < 1000,"X and Y are so big"
        self.x = x-1
        self.y = y-1

        self.laby = []

        for i in range(y):
            self.laby.append([])
            for j in range(x):
                self.laby[i].append([])
                self.laby[i][j] = Case()

    def recup_val(self,x,y) -> int:
        """Get the values of the case of the labyrinth"""
        return(self.laby[y][x].values())

    def bordure_laby(self,x:int,y:int) -> list:
        """Return a list of direction if the case touch a border of the labyrinth"""
        impossible = []
        if x == 0: #Left
            impossible.append(3)
        if y == 0: #Up
            impossible.append(0)
        if x == self.x: #Right
            impossible.append(1)
        if y == self.y: #Down
            impossible.append(2)
        return impossible

    def case_ouverte(self,x:int,y:int) -> bool:
        """Return if the case is open or not"""
        if 0 in self.laby[y][x].values():
            return True
        return False

    def mur_adjacent(self,x:int,y:int) -> list:
        """Return a list of directions if the walls around the case exist"""
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
        """Return a liste of direction if a passage arroud the case exist"""
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
        """Del a wall of a case"""
        self.laby[y][x].change_value(direction,False)
        if direction == 0:
            self.laby[y-1][x].change_value(2,False)
        elif direction == 1:
            self.laby[y][x+1].change_value(3,False)
        elif direction == 2:
            self.laby[y+1][x].change_value(0,False)
        elif direction == 3:
            self.laby[y][x-1].change_value(1,False)

    def ajoute_mur(self,x:int,y:int,direction:int) -> None:
        """Add a wall of a case"""
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
        """Del a wall of a random case linked to a other case has not been opened
        and return his direction, if no wall can be removed, return None"""
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
        """Return the labyrinth in text"""
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
        for i in range(self.x+1):#first line
            if n[i] == "1":
                all += "+-"
            else:
                all += "+ "
        all += "+\n"
        demi = " "
        for i in range((self.y+1)*(self.x+1)):#others lines
            if i % (self.x+1) == 0:# first case of each line
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
            if i % (self.x+1) == self.x:# last case of each line
                all += "\n"+demi+"+\n"
                demi = " "
        return all

def parfait(laby:Labyrinthe):
    """Transform the labyrinth for it become a perfect labyrinth in use a recursiv funtion"""
    recursif_parfait(random.randint(0,laby.x),random.randint(0,laby.y),laby,[])

def recursif_parfait(x:int,y:int,laby,visite) -> None:
    """-if the case is visited, we do nothing
    -else we note like visited and we call the function recursively on each
    of his neighbors not visited after removing the wall with the neighbor"""
    if ((laby.x+1)*(laby.y+1)) != len(visite):
        if [x,y] not in visite:
            visite.append([x,y])
            possible = laby.mur_adjacent(x,y)
            if len(possible) == 0:
                return
            mur_direction = laby.retire_mur_aleatoire(x,y)
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
    """Create a output in a random corner and return his direction"""
    """0=North West/1=North East/2=South East/3=South West"""
    nbr =(random.randint(0,3))
    if nbr == 0:
        laby.laby[0][0].liste[3] = 0
        return(0)
    if nbr == 1:
        laby.laby[0][laby.x].liste[0] = 0
        return(1)
    if nbr == 2:
        laby.laby[laby.y][laby.x].liste[1] = 0
        return(2)
    if nbr == 3:
        laby.laby[laby.y][0].liste[2] = 0
        return(3)

def trouver_sortie(laby:Labyrinthe,out=True) -> int:
    """Return the position of the outpout, (y,x)
    "out" = True return the position of the output
    to the out of the labyrinth"""
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

def tuto()-> Labyrinthe:
    """return the tutorial labyrinth"""
    laby = Labyrinthe(2,2)
    laby.retire_mur(0,0,2)
    laby.retire_mur(1,0,2)
    laby.retire_mur(0,0,1)
    laby.laby[1][0].liste[2] = 0
    return laby

def pos_player(laby) -> tuple:
    """return the position of the player of the begin of a round"""
    s = trouver_sortie(laby,out=False)
    if s == (0,0):#nord ouest
        return(int((laby.y+1)*9/10),int((laby.x+1)*9/10))
    elif s == (0,laby.x):#nord est
        return(int((laby.y+1)*9/10),0)
    elif s == (laby.y,laby.x):#sud est
        return(0,0)
    elif s == (laby.y,0):#sud ouest
        return(0,int((laby.x+1)*9/10))

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad