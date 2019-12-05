import pygame
import time
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.load('./music/BOH.mp3')
# pygame.mixer.music.load('./music/Youkai.mp3')
pygame.mixer.music.play(loops=0, start=0.0)
music = pygame.mixer.Sound("./sound/1.ogg")
music.set_volume(0.8)
music.play()
time.sleep(140)
