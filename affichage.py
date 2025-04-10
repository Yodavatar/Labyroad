#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad

import random
import pygame
from math import atan2,pi
from labyrinthe import trouver_sortie,pos_player

class Affichage():
    def __init__(self,screen,data,laby,time_end,duree,skin,tuto=False,colors=[(20,20,20),(20,20,20)],) -> None:
        self.screen = screen
        self.data = data
        self.laby = laby
        self.tuto = tuto
        
        self.time_end = time_end
        self.duree = duree
        self.clock = 0
        self.speed = 10

        #player
        self.skin=skin
        if tuto:
            self.player = Player((1,1))
            self.charge_tuto()
        else:
            self.player = Player(pos_player(self.laby))
        self.sprite_player = pygame.image.load("assets/sprite/player"+str(self.skin)+".png").convert_alpha()
        self.sprite_player = pygame.transform.scale(self.sprite_player,(self.screen.get_height()/4,self.screen.get_height()/4))
        
        #vision
        self.zoom = 1
        a,b = self.player.position
        self.point_vision = (a+1,b+1)
        
        #time
        self.sprite_time = pygame.image.load("assets/sprite/time.png").convert_alpha()
        self.sprite_time = pygame.transform.scale(self.sprite_time,(self.screen.get_height()/10,self.screen.get_height()/10))
        
        #arrivee
        self.sprite_arrivee = pygame.image.load("assets/sprite/arrivee.png").convert_alpha()
        self.sprite_arrivee = pygame.transform.scale(self.sprite_arrivee,(self.screen.get_height()/4,self.screen.get_height()/4))
        
        #bousole
        self.sprite_boussole = pygame.image.load("assets/sprite/boussole.png").convert_alpha()
        self.sprite_boussole = pygame.transform.scale(self.sprite_boussole,(self.screen.get_height()/20,self.screen.get_height()/20))
        
        #colors
        self.color1 = colors[0]
        self.color2 = colors[1]

        self.load()
        
    def load(self) -> None:
        self.murs_ori = []
        self.murs_ver = []
        self.more_times = []
        if not self.tuto:
            self.sortie = trouver_sortie(self.laby)
            for j in range(0,self.laby.y+1):
                for i in range(0,self.laby.x+1):
                    if random.randint(1,40)==1:
                        self.more_times.append((j,i))
        else:
            self.sortie = (2,0)
            self.more_times.append((0,0))
        

        for y in range(self.laby.y+1): 
            for x in range(self.laby.x+1):
                if self.laby.laby[y][x].values()[0] == 1:
                    self.murs_ori.append((y,x))
                if y == self.laby.y and self.laby.laby[y][x].values()[2] == 1:
                    self.murs_ori.append((y+1,x))
                if self.laby.laby[y][x].values()[3] == 1:
                    self.murs_ver.append((y,x))
                if x == self.laby.x and self.laby.laby[y][x].values()[1] == 1:
                    self.murs_ver.append((y,x+1))
    
    def charge_tuto(self):
        """Load the tutorial text"""
        self.font = pygame.font.Font("assets/font/dialog_font.ttf",int(self.data.moyen_text))
        self.render_1 = self.font.render("Move with the key :",False,(60, 65, 56))
        self.render_2 = self.font.render("[Up] [Down] [Right] [Left]",False,(60, 65, 56))
        self.render_3 = self.font.render("You get 10 sec when",False,(60, 65, 56))
        self.render_4 = self.font.render("you catch a hourglass.",False,(60, 65, 56))
        self.render_5 = self.font.render("Quit the game at all times",False,(60, 65, 56))
        self.render_6 = self.font.render("with [escape]",False,(60, 65, 56))
        self.render_7 = self.font.render("The arrow next to the character",False,(60, 65, 56))
        self.render_8 = self.font.render("indicates always the output.",False,(60, 65, 56))

    def affiche_tuto(self):
        """Show the tutorial"""
        if self.player.position == (1,1):
            self.screen.blit(self.render_1,(self.screen.get_width()*1/3,self.screen.get_height()*3/5))
            self.screen.blit(self.render_2,(self.screen.get_width()*1/3,self.screen.get_height()*3/5+self.screen.get_height()/20))
        elif self.player.position == (0,1):
            self.screen.blit(self.render_3,(self.screen.get_width()*1/3,self.screen.get_height()*3/5))
            self.screen.blit(self.render_4,(self.screen.get_width()*1/3,self.screen.get_height()*3/5+self.screen.get_height()/20))
        elif self.player.position == (0,0):
            self.screen.blit(self.render_5,(self.screen.get_width()*1/3,self.screen.get_height()*3/5))
            self.screen.blit(self.render_6,(self.screen.get_width()*1/3,self.screen.get_height()*3/5+self.screen.get_height()/20))
        elif self.player.position == (1,0):
            self.screen.blit(self.render_7,(self.screen.get_width()*1/3,self.screen.get_height()*3/5))
            self.screen.blit(self.render_8,(self.screen.get_width()*1/3,self.screen.get_height()*3/5+self.screen.get_height()/20))

    def deplacement(self,direction):
        """The movement of the player with his direction"""
        if direction == 0 and self.can_move(0):
            self.player.haut()
            self.camera()
            self.bonus()
            self.update()
        elif direction == 1 and self.can_move(1):
            self.player.droite()
            self.camera()
            self.bonus()
            self.update()
        elif direction == 2 and self.can_move(2):
            self.player.bas()
            self.camera()
            self.bonus()
            self.update()
        elif direction == 3 and self.can_move(3):
            self.player.gauche()
            self.camera()
            self.bonus()
            self.update()
        return self.sortie == self.player.position
    
    def color_new(self,min_c,max_c,pos_x,pos_y,t):
        """return the medium of 2 colors compared to the position of the player"""
        return((max_c-min_c)*(pos_x+pos_y)/t)+min_c

    def color_degrad(self,pos_x,pos_y):
        """return a tuple of color with position x and y with (r,g,b)"""
        tab = []
        for i in range(3):
            if self.color1[i]<self.color2[i]:
                tab.append(self.color_new(self.color1[i],self.color2[i],pos_x,pos_y,self.laby.x+self.laby.y+2))
            else:
                tab.append(self.color_new(self.color2[i],self.color1[i],pos_x,pos_y,self.laby.x+self.laby.y+2))
        return (int(tab[0]),int(tab[1]),int(tab[2]))

    def bonus(self) -> None:
        """Check if the player is on a case of bonus"""
        j,i = self.player.position
        for y,x in self.more_times:
            if j == y and i == x:
                self.more_times.remove((y,x))
                self.time_end += 10000

    def camera(self) -> None:
        """If the player is out of the center of the screen 2*2
        we move the camera"""
        if not self.tuto:
            j,i = self.point_vision
            y,x = self.player.position
            if not j-1 <= y <= j or not i-1 <= x <= i:
                if y < j-1:
                    j -= 1
                elif y > j:
                    j += 1
                elif x < i-1:
                    i -= 1
                elif x > i:
                    i += 1
            self.point_vision = (j,i)

    def can_move(self,direction):
        """Check if the player can move"""
        y,x = self.player.position
        if direction == 0:
            return self.laby.laby[y][x].values()[0] == 0
        elif direction == 1:
            return self.laby.laby[y][x].values()[1] == 0
        elif direction == 2:
            return self.laby.laby[y][x].values()[2] == 0
        elif direction == 3:
            return self.laby.laby[y][x].values()[3] == 0

    def time(self) -> bool:
        """Write the timer on the screen, return is the time is over"""
        pourcentage = (self.time_end - pygame.time.get_ticks()) / self.duree
        time = [0,0,int(pourcentage*self.screen.get_width()),int(self.screen.get_width()/60)]
        pygame.draw.rect(self.screen,(20,20,20),[0,0,self.screen.get_width(),int(self.screen.get_width()/60)])
        pygame.draw.rect(self.screen,(193, 102, 224),time)
        return self.time_end - pygame.time.get_ticks() <= 0

    def angle_boussole(self) -> float:
        '''Return the direction of the output in degree comparated to the output'''
        y2,x2 = self.player.position
        y1,x1 = self.sortie
        return 180-atan2((y2-y1),(x2-x1))/pi*180

    def boussole(self) -> pygame.sprite:
        """Change the degree of the compass to the output"""
        return pygame.transform.rotate(self.sprite_boussole, self.angle_boussole()-90)

    def update(self) -> None:
        """Update the loop of the game"""
        pygame.draw.rect(self.screen,(248,228,255),[0,0,self.screen.get_width(),self.screen.get_height()])
        pygame.display.flip()
        if self.zoom == 1:
            dist_vert = self.screen.get_height()/4
            dist_oriz = self.screen.get_width()/4
            court_vert = int(dist_vert/16)
            court_oriz = int(dist_oriz/16)

            j,i = self.point_vision
            for y,x in self.murs_ver:
                if j-2 <= y <= j+2 and i-2 <= x <=i+2:
                    pygame.draw.rect(self.screen,self.color_degrad(x,y),[self.screen.get_width()/2+((x-i)*dist_oriz)-court_oriz/2,self.screen.get_height()/2+((y-j)*dist_vert)-court_vert/2,court_oriz,dist_vert])
            
            for y,x in self.murs_ori:
                if j-2 <= y <= j+2 and i-2 <= x <=i+2:
                    pygame.draw.rect(self.screen,self.color_degrad(x,y),[self.screen.get_width()/2+((x-i)*dist_oriz)-court_oriz/2,self.screen.get_height()/2+((y-j)*dist_vert)-court_vert/2,dist_oriz,court_vert])
            
            y,x = self.player.position
            self.screen.blit(self.sprite_player,(self.screen.get_width()/2+((x-i)*dist_oriz),self.screen.get_height()/2+((y-j)*dist_vert)))
            self.screen.blit(self.boussole(),(self.screen.get_width()/2+((x-i)*dist_oriz+dist_oriz/2),self.screen.get_height()/2+((y-j)*dist_vert)+dist_vert/2))
            
            for y,x in self.more_times:
                if j-2 <= y <= j+1 and i-2 <= x <=i+1:
                    self.screen.blit(self.sprite_time,(self.screen.get_width()/2+((x-i)*dist_oriz)+dist_oriz/3,self.screen.get_height()/2+((y-j)*dist_vert)+dist_vert/3))

            y,x = self.sortie
            self.screen.blit(self.sprite_arrivee,(self.screen.get_width()/2+((x-i)*dist_oriz),self.screen.get_height()/2+((y-j)*dist_vert)))            

            if self.tuto:
                self.affiche_tuto()

class Player():
    def __init__(self,position) -> None:
        """Player class who have position in (y,x)"""
        self.position = position
    def haut(self):
        """edit position with y-1"""
        self.y,self.x = self.position
        self.position = (self.y-1,self.x)
    def bas(self):
        """edit position with y+1"""
        self.y,self.x = self.position
        self.position = (self.y+1,self.x)
    def droite(self):
        """edit position with x+1"""
        self.y,self.x = self.position
        self.position = (self.y,self.x+1)
    def gauche(self):
        """edit position with x-1"""
        self.y,self.x = self.position
        self.position = (self.y,self.x-1)

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad