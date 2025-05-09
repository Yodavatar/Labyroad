#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad

import pygame
from labyrinthe import *
from song import*
from data import*
from affichage import*

class Game():
    def __init__(self) -> None:
        """Load the game"""
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.data = Donnee(self.screen)
        self.data.recuperer()
        INITIAL(self.screen,self.data)
        self.song = Song()
        self.continu = False
        self.page_end = End(self.screen,self.data)

    def go_to_home(self) -> None:
        """begin the home page."""    
        home = Home(self.screen,self.song,self.data)
        self.choose_game,self.skin = home.run()
        if self.choose_game == 0:#quit
            pygame.quit()
        elif self.choose_game == 1:#easy
            self.charge_laby()
        elif self.choose_game == 2:#normal
            self.charge_laby()
        elif self.choose_game == 3:#difficult
            self.charge_laby()
        elif self.choose_game == 4:#tuto
            self.charge_laby()

    def charge_laby(self)-> None:
        """begin the game"""
        if self.choose_game == 4:#tutorial / black labyrinth
            self.screen.fill((248, 228, 255))
            self.laby = tuto()
            self.sortie = (2,0)
            self.running = True
            self.song.play("tuto",root="assets/music/level/")
            self.time_end = pygame.time.get_ticks()+30000
            self.affichage = Affichage(self.screen,self.data,self.laby,self.time_end,30000,skin=self.skin,tuto=True,colors=[(155,155,155),(0,0,0)])
            self.run()
        
        elif self.choose_game == 1:#easy / blue labyrinth
            self.screen.fill((248, 228, 255))
            self.laby = Labyrinthe(10,10)
            parfait(self.laby)
            creer_sortie(self.laby)
            self.song.play("kingdom",root="assets/music/level/")
            self.time_end = pygame.time.get_ticks()+50000
            self.affichage = Affichage(self.screen,self.data,self.laby,self.time_end,50000,skin=self.skin,colors=[(89, 31, 206),(61, 189, 194)])
            self.run()
        
        elif self.choose_game == 2:#normal / green labyrinth
            self.screen.fill((248, 228, 255))
            self.laby = Labyrinthe(15,15)
            parfait(self.laby)
            creer_sortie(self.laby)
            self.song.play("normal",root="assets/music/level/")
            self.time_end = pygame.time.get_ticks()+55000
            self.affichage = Affichage(self.screen,self.data,self.laby,self.time_end,55000,skin=self.skin,colors=[(27, 65, 8),(196, 232, 178)])
            self.run()

        elif self.choose_game == 3:#difficult / red labyrinth
            self.screen.fill((248, 228, 255))
            self.laby = Labyrinthe(20,20)
            parfait(self.laby)
            creer_sortie(self.laby)
            self.song.play("epic",root="assets/music/level/",begin=30)
            self.time_end = pygame.time.get_ticks()+60000
            self.affichage = Affichage(self.screen,self.data,self.laby,self.time_end,60000,skin=self.skin,colors=[(193, 168, 129),(127, 17, 17)])
            self.run()
    
    def end(self,result) -> None:
        """message if the game is over"""
        if not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)
        if result:
            if self.choose_game == 1:
                self.data.victoire_easy += 1
            elif self.choose_game == 2:
                self.data.victoire_normal +=1
            elif self.choose_game == 3:
                self.data.victoire_difficile +=1
        else:
            if self.choose_game == 1:
                self.data.defaite_easy += 1
            elif self.choose_game == 2:
                self.data.defaite_normal +=1
            elif self.choose_game == 3:
                self.data.defaite_difficile +=1
        self.data.sauvegarder()
        if self.choose_game != 4:
            self.continu = self.page_end.run(self.choose_game,result)
        else:
            self.continu = True
        self.running = False

    def run(self) -> None:
        """loop of the game"""
        self.running = True
        self.affichage.update()
        if pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        if self.affichage.deplacement(0) == True:
                            self.end(True)
                    elif event.key == pygame.K_RIGHT:
                        if self.affichage.deplacement(1) == True:
                            self.end(True)
                    elif event.key == pygame.K_DOWN:
                        if self.affichage.deplacement(2) == True:
                            self.end(True)
                    elif event.key == pygame.K_LEFT:
                        if self.affichage.deplacement(3) == True:
                            self.end(True)
            
            if self.running:
                self.clock.tick(10)  # limits FPS
                pygame.display.flip() #update of pygame
                if self.affichage.time():
                    self.end(False)
            
        
        if self.continu:
            self.go_to_home()        
        else:
            pygame.quit()

class End():
    def __init__(self,screen,data) -> None:
        """Init"""
        self.continu = True
        self.screen = screen
        self.data = data

        self.ecart = self.screen.get_width()/200
        #buttons non clickable
        self.bloc_fond = [self.screen.get_width()*1/3/2,self.screen.get_height()*1/3/2,self.screen.get_width()*2/3,self.screen.get_height()*2/3]
        self.bloc_principale = [self.screen.get_width()*1/3/2+self.ecart,self.screen.get_height()*1/3/2+self.ecart,self.screen.get_width()*2/3-2*self.ecart,self.screen.get_height()*2/3-2*self.ecart]

        #buttons clickable
        self.rect_continu = [self.screen.get_width()*1/3/2+self.screen.get_width()*2/3/9,self.screen.get_height()*2/3,self.screen.get_width()*2/3/3,self.screen.get_height()/8]
        self.rect_quit = [self.screen.get_width()*1/3/2+self.screen.get_width()*2/3/9*2+self.screen.get_width()*2/3/3,self.screen.get_height()*2/3,self.screen.get_width()*2/3/3,self.screen.get_height()/8]

        #colors
        self.color_black =  (39, 40, 41)
        self.color_blue = (97, 103, 122)
        self.color_white = (240, 232, 242)

        #Font
        self.font = pygame.font.Font("assets/font/dialog_font.ttf",int(self.data.taille_text*1.25))

        #Write the text
        self.render_continu = self.font.render("Continue",False,self.color_blue)
        self.render_quit = self.font.render("Quit",False,self.color_blue)

    def charge_phrase(self) -> None:
        """Load the sentence"""
        if self.result:
            self.render1 = self.font.render("You have win !",False,(0,0,0))
        else:
            self.render1 = self.font.render("You have lose !",False,(0,0,0))
        if self.level == 1:
            p = self.data.victoire_easy/(self.data.victoire_easy+self.data.defaite_easy)
        elif self.level == 2:
            p = self.data.victoire_normal/(self.data.victoire_normal+self.data.defaite_normal)
        else:
            p = self.data.victoire_difficile/(self.data.victoire_difficile+self.data.defaite_difficile)
        p = str(int(p*100))
        self.render2 = self.font.render("Pourcentage de victoire : "+p+"%.",False,(0,0,0))

    def button(self,bloc) -> None:
        """Show the button"""
        if self.souris_on_button(bloc):
            pygame.draw.rect(self.screen,self.color_blue,bloc)
        else:
            pygame.draw.rect(self.screen,self.color_black,bloc)

    def souris_on_button(self,bloc):
        """Check if the mouse is on the button"""
        return bloc[0]<pygame.mouse.get_pos()[0]<bloc[0]+bloc[2] and bloc[1]<pygame.mouse.get_pos()[1]<bloc[1]+bloc[3]

    def run(self,level,result):
        """return True if the player want to continue the game"""
        self.running = True
        self.level = level
        self.result = result
        self.charge_phrase()
        if not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.souris_on_button(self.rect_continu):
                            self.running = False
                            self.continu = True
                        elif self.souris_on_button(self.rect_quit):
                            self.running = False
                            self.continu = False
            if self.running:
                pygame.draw.rect(self.screen,self.color_black,self.bloc_fond)
                pygame.draw.rect(self.screen,self.color_white,self.bloc_principale)

                self.button(self.rect_continu)
                self.button(self.rect_quit)

                """writing"""
                self.screen.blit(self.render1,(self.screen.get_width()*1/3/2+self.screen.get_width()/200,self.screen.get_height()*1/3/2))
                self.screen.blit(self.render2,(self.screen.get_width()*1/3/2+self.screen.get_width()/200,self.screen.get_height()*1/3/2+self.screen.get_height()/10))
                
                self.screen.blit(self.render_continu,(self.rect_continu[0],self.rect_continu[1]))
                self.screen.blit(self.render_quit,(self.rect_quit[0],self.rect_quit[1]))
                
                pygame.display.flip() #Update of pygame
        return self.continu

class Home():
    def __init__(self,screen,song,data) -> None:
        """page of the game"""
        self.screen = screen
        self.song = song
        self.data = data
        self.song.play("calme",root="assets/music/intro/",begin=10)
        self.running = True
        self.font_grand = pygame.font.Font("assets/font/dialog_font.ttf",int(self.data.taille_text*1.5))
        self.font_moyen = pygame.font.Font("assets/font/dialog_font.ttf",int(self.data.taille_text*1.25))
        self.welcome = self.font_grand.render("Welcome on LabyRoad",False,(255, 246, 224))
        self.num_skin = 1

        """Color of the UI"""
        self.color_black = (39, 40, 41)
        self.color_blue = (97, 103, 122)
        self.color_grey = (216, 217, 218)
        self.color_white = (255, 246, 224)

        """values"""
        self.normal_value = int(self.screen.get_width()/180)
        self.unite = int(self.screen.get_width()/12)

        self.ecart_width = int(self.screen.get_width()*1/2*1/5*1/2)
        self.bloc_width = int(self.screen.get_width()*1/2*4/5)

        self.ecart_height = int(self.screen.get_height()*4/5*2/6/5)
        self.bloc_height = int(self.screen.get_height()*4/5/6)

        """Buttons clickable"""
        self.rect_facile = [self.ecart_width,self.ecart_height+self.screen.get_height()/5,self.bloc_width,self.bloc_height]
        self.rect_normal = [self.ecart_width,self.bloc_height+self.ecart_height*2+self.screen.get_height()/5,self.bloc_width,self.bloc_height]
        self.rect_difficile = [self.ecart_width,self.bloc_height*2+self.ecart_height*3+self.screen.get_height()/5,self.bloc_width,self.bloc_height]
        self.rect_tuto = [self.ecart_width,self.bloc_height*3+self.ecart_height*4+self.screen.get_height()/5,self.bloc_width/2-self.ecart_width/2,self.bloc_height]
        self.rect_skin = [self.ecart_width*2+self.bloc_width/2-self.ecart_width/2,self.bloc_height*3+self.ecart_height*4+self.screen.get_height()/5,self.bloc_width/2-self.ecart_width/2,self.bloc_height]
        self.rect_quit = [int(self.screen.get_width()*9.5/10),0,int(self.screen.get_width()*0.5/10),int(self.screen.get_width()*0.5/10)]

        """Load the font"""
        self.render_facile = self.font_grand.render("Easy",False,(121, 226, 224))
        self.render_normal = self.font_grand.render("Normal",False,(159, 234, 114))
        self.render_difficile = self.font_grand.render("Difficult",False,(233, 66, 89))
        self.render_quit = self.font_moyen.render("X",False,self.color_white)
        self.render_tuto = self.font_moyen.render("Tutorial",False,(60, 65, 56))
        self.render_skin = self.font_moyen.render("Skin",False,(60, 65, 56))

        """Load the skin"""
        self.charge_skin()

    def button(self,bloc) -> None:
        """Show the button"""
        if self.souris_on_button(bloc):
            pygame.draw.rect(self.screen,self.color_blue,bloc)
        else:
            pygame.draw.rect(self.screen,self.color_black,bloc)

    def souris_on_button(self,bloc):
        """Check if the mouse is on button"""
        return bloc[0]<pygame.mouse.get_pos()[0]<bloc[0]+bloc[2] and bloc[1]<pygame.mouse.get_pos()[1]<bloc[1]+bloc[3]

    def charge_skin(self):
        """Load the new player and hide the old"""
        self.skin = pygame.image.load("assets/sprite/player"+str(self.num_skin)+".png").convert_alpha()
        self.sprite_player = pygame.transform.scale(self.skin,(self.screen.get_height()/2,self.screen.get_height()/2))
        self.screen.fill((107,114,142))

    def run(self):
        """The loop of the game"""
        if pygame.mouse.get_visible() == False:
            pygame.mouse.set_visible(True)
        self.screen.fill((107, 114, 142))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Transition(self.screen,self.song)
                        choose_game = 0
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.souris_on_button(self.rect_facile):
                            Transition(self.screen,self.song)
                            choose_game = 1
                            self.running = False
                        elif self.souris_on_button(self.rect_normal):
                            Transition(self.screen,self.song)
                            choose_game = 2
                            self.running = False
                        elif self.souris_on_button(self.rect_difficile):
                            Transition(self.screen,self.song)
                            choose_game = 3
                            self.running = False
                        elif self.souris_on_button(self.rect_tuto):
                            Transition(self.screen,self.song)
                            choose_game = 4
                            self.running = False
                        elif self.souris_on_button(self.rect_skin):
                            if self.num_skin <4:
                                self.num_skin +=1
                            else:
                                self.num_skin = 1
                            self.charge_skin()
                        elif self.souris_on_button(self.rect_quit):
                            choose_game = 0
                            self.running = False  

            if self.running:
                """non clickable button"""
                pygame.draw.rect(self.screen,self.color_black,[0,0,self.screen.get_width(),self.screen.get_height()/5])
                """clickable button"""
                self.button(self.rect_facile)
                self.button(self.rect_normal)
                self.button(self.rect_difficile)
                self.button(self.rect_tuto)
                self.button(self.rect_skin)
                self.button(self.rect_quit)

                """Welcome write"""
                self.screen.blit(self.welcome,(self.screen.get_width()/5,self.screen.get_height()/12))
                self.screen.blit(self.render_facile,(self.rect_facile[0],self.rect_facile[1]))
                self.screen.blit(self.render_normal,(self.rect_normal[0],self.rect_normal[1]))
                self.screen.blit(self.render_difficile,(self.rect_difficile[0],self.rect_difficile[1]))
                self.screen.blit(self.render_tuto,(self.rect_tuto[0],self.rect_tuto[1]))
                self.screen.blit(self.render_skin,(self.rect_skin[0],self.rect_skin[1]))
                self.screen.blit(self.render_quit,(self.rect_quit[0]+int(self.screen.get_width()*0.5/10)/4,self.rect_quit[1]+int(self.screen.get_width()*0.5/10)/8))

                """update the element"""
                self.screen.blit(self.sprite_player,(self.screen.get_width()/2,self.screen.get_height()/5))
                pygame.display.flip()    
        return choose_game,self.num_skin

class INITIAL():
    def __init__(self,screen,donnee):
        """The effect of the beginning of the game"""
        pygame.mixer.music.load("assets/music/intro/studio-quaerite.ogg")#futuristic-logo-3-versions.ogg / rock-cinematic.ogg / studio-quaerite.ogg
        pygame.mixer.music.play()
        font = pygame.font.Font("assets/font/dialog_font.ttf",donnee.taille_text)
        msg_white = font.render("Studio-Quaerite",False,(255,255,255))
        msg_black = font.render("Studio-Quaerite",False,(0,0,0))
        if pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)
        while pygame.mixer.music.get_busy():
            if  8000 < pygame.mixer.music.get_pos() < 14000:
                rayon = (pygame.mixer.music.get_pos() - 8000) * screen.get_width() / 200
                pygame.draw.circle(screen,(255,255,255),(int(screen.get_width()/2),int(screen.get_height()/2)),rayon)
                screen.blit(msg_black,(screen.get_width()/3,screen.get_height()/2))
            else:
                screen.blit(msg_white,(screen.get_width()/3,screen.get_height()/2))
            pygame.display.flip()
        if pygame.mouse.get_visible() == False:
            pygame.mouse.set_visible(True)

class Transition():
    def __init__(self,screen,song) -> None:    
        """Little transition when a click of the player"""
        song.play("radio",root="assets/music/bruitage/",loops=1)
        if pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)
        while pygame.mixer.music.get_busy():
            rayon = (pygame.mixer.music.get_pos() - 1500) * screen.get_width() / 3000
            rayon2 = (pygame.mixer.music.get_pos() - 1500) * screen.get_width() / 6000

            pygame.draw.circle(screen,(80,87,122),pygame.mouse.get_pos(),rayon)
            pygame.draw.circle(screen,(71,78,104),pygame.mouse.get_pos(),rayon2)
            pygame.display.flip()
        if pygame.mouse.get_visible() == False:
            pygame.mouse.set_visible(True)

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad