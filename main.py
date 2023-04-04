from glob import glob
import pygame
from pygame.locals import *
from sys import exit
from random import randint
import math

pygame.init()

# programIcon = pygame.image.load('snake.png')
# pygame.display.set_icon(programIcon)

pygame.mixer.music.set_volume(0.2)
musica_de_fundo = pygame.mixer.music.load('to_me.mp3')
pygame.mixer.music.play(start=10, loops=-1, fade_ms=1000)
barulho_colisao = pygame.mixer.Sound('collectcoin.wav')
largura = 800
altura = 600
tamanho_objeto = 16
pontos = 0
recorde = 0
fonte = pygame.font.SysFont("Arial", 20, True, True)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobrinha')
relogio = pygame.time.Clock()
velocidade = tamanho_objeto

x_maca = 0
y_maca = 0
x_cobra = 0
y_cobra = 0


def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], tamanho_objeto, tamanho_objeto))


def reiniciar_jogo():
    global x_cobra, y_cobra, x_maca, y_maca, x_controle, y_controle, pontos, comprimeto_cobra, lista_cabeca, lista_cobra, morreu
    pontos = 0
    comprimeto_cobra = 1
    spawn_cobra()
    x_controle = 0
    y_controle = 0
    spawn_maca()
    lista_cobra = []
    lista_cabeca = []
    morreu = False
    pygame.mixer.music.play(start=10, loops=-1, fade_ms=1000)


def spawn_maca():
    global x_maca, y_maca
    coord = randint(0, largura - tamanho_objeto)
    x_maca = coord - coord % tamanho_objeto
    coord = randint(0, altura - tamanho_objeto)
    y_maca = coord - coord % tamanho_objeto


def pinta_tela():
    tela.fill((240, 240, 240))


def spawn_cobra():
    global x_cobra, y_cobra
    x_cobra = (int(largura / 2) - int(tamanho_objeto / 2)) - (
                int(largura / 2) - int(tamanho_objeto / 2)) % tamanho_objeto
    y_cobra = (int(altura / 2) - int(tamanho_objeto / 2)) - (int(altura / 2) - int(tamanho_objeto / 2)) % tamanho_objeto


def death_screen():
    global pontos, recorde
    pinta_tela()
    if pontos > recorde:
        recorde = pontos
    font2 = pygame.font.SysFont("Arial", 20, True, True)
    texto = font2.render("Erroooou! Pressione r para recomeçar...", True, (0, 0, 0))
    tela.blit(texto, (int(largura / 2 - texto.get_width() / 2), int(altura / 2 - texto.get_height() / 2)))
    texto = font2.render("Você fez {} pontos. O recorde é {} pontos.".format(pontos, recorde), True, (0, 0, 0))
    tela.blit(texto, (int(largura / 2 - texto.get_width() / 2), int(altura / 2 - texto.get_height() / 2) + 50))
    pygame.display.flip()


x_controle = 0
y_controle = 0

spawn_maca()
spawn_cobra()

lista_cobra = []
comprimeto_cobra = 1

morreu = False
mudo = False

while True:
    pinta_tela()
    relogio.tick(15 + int(pontos / 5))  # velocidade aumenta 1 a cada 5 pontos
    mensagem = fonte.render("Pontos: {}".format(pontos), True, (0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_m:
                if mudo:
                    pygame.mixer.music.unpause()
                    mudo = False
                else:
                    pygame.mixer.music.pause()
                    mudo = True

            if event.key == K_LEFT:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_RIGHT:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_UP:
                if y_controle == velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = -velocidade
            if event.key == K_DOWN:
                if y_controle == -velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = velocidade

    x_cobra += x_controle
    y_cobra += y_controle

    cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, tamanho_objeto, tamanho_objeto))
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, tamanho_objeto, tamanho_objeto))
    # maca = pygame.draw.circle(tela, (255, 0, 0), [x_maca, y_maca], tamanho_objeto/2)

    if cobra.colliderect(maca):
        spawn_maca()
        barulho_colisao.play()
        comprimeto_cobra += 1
        pontos += 1

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)

    lista_cobra.append(lista_cabeca)

    if len(lista_cobra) > comprimeto_cobra:
        del lista_cobra[0]

        if lista_cobra.count(lista_cabeca) > 1:
            morreu = True
            death_screen()
        if x_cobra < 0 or x_cobra > largura - tamanho_objeto or y_cobra < 0 or y_cobra > altura - tamanho_objeto:
            morreu = True
            death_screen()

        while morreu:
            pygame.mixer.music.stop()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()

            pygame.display.flip()

    if not morreu:
        aumenta_cobra(lista_cobra)

    tela.blit(mensagem, (16, 16))
    # pygame.draw.circle(tela, (0, 255, 0), (100, 100), 10)
    # pygame.draw.line(tela, (0, 0, 255), (0, 0), (100, 100), 2)
    font3 = pygame.font.SysFont("Arial", 10, False, True)
    log = font3.render("Cobra: x{} y{} | Maca: x{} y{} | Velocidade: {}".format(x_cobra, y_cobra, x_maca, y_maca,
                                                                                15 + int(pontos / 5)), True, (0, 0, 0))
    tela.blit(log, (20, 570))

    pygame.display.flip()