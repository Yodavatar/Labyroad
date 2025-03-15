#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad

import pygame

class Song():
    def __init__(self):
        """Gestion des pistes audio"""
        self.volume = 1
        pygame.mixer.init()

    def play(self,name,root="assets/music/",loops=-1,begin=0):
        """Lance la musique, doit etre au format .ogg"""
        pygame.mixer.music.load(root+name+".ogg")
        pygame.mixer.music.play(loops,fade_ms=1000,start=begin)
        pygame.mixer.music.set_volume(self.volume)

    def stop(self)->None:
        """arrete le musique en cours"""
        pygame.mixer.stop()
    
    def change_volume(self,volume)->None:
        """change le volume"""
        pygame.mixer.music.set_volume(volume)
        self.volume = volume

    def more_volume(self):
        """augmente le volume de 0.05"""
        if self.volume == 1:
            pass
        else:
            self.volume +=0.05
            pygame.mixer.music.set_volume(self.volume)

    def less_volume(self):
        """descend le volume de 0.05"""
        if self.volume == 0:
            pass
        else:
            self.volume -= 0.05
            pygame.mixer.music.set_volume(self.volume)

#Coding : utf-8
#Coding by Yodavatar
#Licensed code CC BY-NC-SA 4.0
#Jeu : LabyRoad