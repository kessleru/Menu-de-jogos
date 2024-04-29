import tkinter as tk
import pygame, random
import random
from tkinter import *
from tkinter import ttk
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice


#Variáveis do jogo da forca 
jogador_1 = 'X'
jogador_2 = 'O'

score_1 = 0 
score_2 = 0

joga = ''
contador  = 0
contador_rodada = 0
jogando = 'X'

#Variáveis do Flappy Bird
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200


#Menu de jogos
class MenuJogos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu de Jogos")
        self.geometry("500x400")

        self.label = tk.Label(self, text="Escolha um jogo:")
        self.label.pack(pady=10)

        self.btn_forca = tk.Button(self, text="Jogo da velha", command=self.jogar_velha)
        self.btn_forca.pack(pady=10)

        self.btn_cobrinha = tk.Button(self, text="Jogo da cobrinha", command=self.jogar_cobrinha)
        self.btn_cobrinha.pack()

        self.btn_flappy = tk.Button(self, text="Jogo do flappy bird", command=self.jogar_flappy)
        self.btn_flappy.pack(pady=10)

        self.btn_dino = tk.Button(self, text="Jogo do Dino", command=self.jogar_dino)
        self.btn_dino.pack()


    def jogar_dino(self):

        pygame.init()
        pygame.mixer.init()

        diretorio_principal = os.path.dirname(__file__)
        diretorio_imagens = os.path.join(diretorio_principal, 'imagens')


        # ao iniciar ações, para-las

        LARGURA = 640
        ALTURA = 480

        BRANCO = (255,255,255)

        tela = pygame.display.set_mode((LARGURA, ALTURA))

        pygame.display.set_caption('Dino Game')

        sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()

        colidiu = False

        escolha_obstaculo = choice([0, 1])

        pontos = 0

        velocidade_jogo = 10

        def exibe_mensagem(msg, tamanho, cor):
            fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
            mensagem = f'{msg}' # f-format
            texto_formatado = fonte.render(mensagem, True, cor)
            return texto_formatado

        def reiniciar_jogo():
            global pontos, velocidade_jogo, colidiu, escolha_obstaculo
            pontos = 0
            velocidade_jogo = 10
            colidiu = False
            dino.rect.y = ALTURA - 64 - 96//2
            dino.pulo = False
            dino_voador.rect.x = LARGURA
            cacto.rect.x = LARGURA
            escolha_obstaculo = choice([0, 1])

        class Dino(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagens_dinossauro = []
                for i in range(3):
                    img = sprite_sheet.subsurface((i * 32,0), (32,32)) # recortar frame do spriteSheet
                    img = pygame.transform.scale(img, (32*3, 32*3))
                    self.imagens_dinossauro.append(img)

                self.index_lista = 0
                self.image = self.imagens_dinossauro[self.index_lista]
                self.rect = self.image.get_rect()
                self.mask = pygame.mask.from_surface(self.image)
                self.pos_y_inicial = ALTURA - 64 - 96//2
                self.rect.topleft = (100, self.pos_y_inicial) #368 416(centro y)
                self.pulo = False

            def pular(self):
                self.pulo = True


            def update(self): #alterar posição y 
                if self.pulo == True:
                    if self.rect.y <= self.pos_y_inicial - 150:
                        self.pulo = False
                    self.rect.y -= 15

                else:
                    if self.rect.y >= self.pos_y_inicial:
                        self.rect.y = self.pos_y_inicial
                    else:
                        self.rect.y += 15


                if self.index_lista > 2:
                    self.index_lista = 0
                self.index_lista += 0.25
                self.image = self.imagens_dinossauro[int(self.index_lista)]

        class Nuvens(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
                self.image = pygame.transform.scale(self.image, (32*3, 32*3))
                self.rect = self.image.get_rect()
                self.rect.y = randrange(50, 200, 50) #definir posição aleatoria da nuvem, vai sortear um numero entre 50 e 200 variando de 50 em 50
                self.rect.x = LARGURA - randrange(30, 300, 90)

            def update(self): #movimentar nuvem apenas no eixo x
                if self.rect.topright[0] < 0: #posição superior direita
                    self.rect.x = LARGURA
                    self.rect.y = randrange(50, 200, 50)
                self.rect.x -= velocidade_jogo

        class Chao(pygame.sprite.Sprite):
            def __init__(self, pos_x):
                pygame.sprite.Sprite.__init__(self)
                self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
                self.image = pygame.transform.scale(self.image, (32*2, 32*2))
                self.rect = self.image.get_rect()
                self.rect.y = ALTURA - 64
                self.rect.x = pos_x * 64

            def update(self):
                if self.rect.topright[0] < 0:
                    self.rect.x = LARGURA
                self.rect.x -= 10

        class Cacto(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
                self.image = pygame.transform.scale(self.image, (32*2, 32*2))
                self.rect = self.image.get_rect()
                self.mask = pygame.mask.from_surface(self.image)
                self.escolha = escolha_obstaculo
                self.rect.center = (LARGURA, ALTURA - 64)
                self.rect.x = LARGURA

            def update(self):
                if self.escolha == 0:
                    if self.rect.topright[0] < 0:
                        self.rect.x = LARGURA
                    self.rect.x -= velocidade_jogo

        class DinoVoador(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagens_dinossauro = []
                for i in range(3,5):
                    img = sprite_sheet.subsurface((i*32, 0), (32,32))
                    img = pygame.transform.scale(img, (32*3, 32*3))
                    self.imagens_dinossauro.append(img)

                self.index_lista = 0
                self.image = self.imagens_dinossauro[self.index_lista]
                self.mask = pygame.mask.from_surface(self.image)
                self.escolha = escolha_obstaculo
                self.rect = self.image.get_rect()
                self.rect.center = (LARGURA, 300)
                self.rect.x = LARGURA

            def update(self):
                if self.escolha == 1:
                    if self.rect.topright[0] < 0:
                        self.rect.x = LARGURA
                    self.rect.x -= velocidade_jogo

                    if self.index_lista > 1:
                        self.index_lista = 0
                    self.index_lista += 0.25
                    self.image = self.imagens_dinossauro[int(self.index_lista)]

        todas_as_sprites = pygame.sprite.Group()
        dino = Dino()
        todas_as_sprites.add(dino)

        for i in range(4):
            nuvem = Nuvens()
            todas_as_sprites.add(nuvem)

        for i in range(LARGURA*2//64):
            chao = Chao(i)
            todas_as_sprites.add(chao)

        cacto = Cacto()
        todas_as_sprites.add(cacto)

        dino_voador = DinoVoador()
        todas_as_sprites.add(dino_voador)

        grupo_obstaculos = pygame.sprite.Group()
        grupo_obstaculos.add(cacto)
        grupo_obstaculos.add(dino_voador)

        relogio = pygame.time.Clock()
        while True:
            relogio.tick(30)
            tela.fill(BRANCO)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE and colidiu == False:
                        if dino.rect.y != dino.pos_y_inicial:
                            pass
                        else:
                            dino.pular()

                    if event.key == K_r and colidiu == True:
                        reiniciar_jogo()

            colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask) # utilizar comando dentro do loop principal do jogo, lista inicia vazia e quando colide recebe o obj

            todas_as_sprites.draw(tela)

            if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
                escolha_obstaculo = choice([0, 1])
                cacto.rect.x = LARGURA
                dino_voador.rect.x = LARGURA
                cacto.escolha = escolha_obstaculo
                dino_voador.escolha = escolha_obstaculo

            if colisoes and colidiu == False: 
                colidiu = True

            if colidiu == True:
                if pontos % 100 == 0:
                    pontos += 1
                game_over = exibe_mensagem('GAME OVER', 40, (0,0,0)) #essa função tem um retorno, então tem que ter uma var para recebe-lo
                tela.blit(game_over, (LARGURA//2, ALTURA//2))
                restart = exibe_mensagem('Pressione r para reiniciar', 20, (0,0,0))
                tela.blit(restart, (LARGURA//2, (ALTURA//2) + 60))

            else:
                pontos += 1 # só incrementa pontos se não houver colisãomemor
                todas_as_sprites.update()
                texto_pontos = exibe_mensagem(pontos, 40, (0,0,0))

            if pontos % 100 == 0: # a cada 100 pontos aumenta a velocidade, é feito pelo resto da divisão por 100
                if velocidade_jogo >= 23:
                    velocidade_jogo += 0
                else:
                    velocidade_jogo += 1

            tela.blit(texto_pontos, (520, 30))

            pygame.display.flip()



    #Flappy Bird
    def jogar_flappy(self):
        class Bird(pygame.sprite.Sprite):

            def __init__(self):
                pygame.sprite.Sprite.__init__(self)

                self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                            pygame.image.load('bluebird-midflap.png').convert_alpha(),
                            pygame.image.load('bluebird-downflap.png').convert_alpha()]

                self.speed = SPEED

                self.current_image = 0

                self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
                self.mask = pygame.mask.from_surface(self.image)

                self.rect = self.image.get_rect()
                self.rect[0] = SCREEN_WIDTH / 2
                self.rect[1] = SCREEN_HEIGHT / 2

            def update(self):
                self.current_image = (self.current_image + 1) % 3
                self.image = self.images[ self.current_image ]

                self.speed += GRAVITY

                # Update height
                self.rect[1] += self.speed

            def bump(self):
                self.speed = -SPEED

        class Pipe(pygame.sprite.Sprite):

            def __init__(self, inverted, xpos, ysize):
                pygame.sprite.Sprite.__init__(self)

                self.image = pygame.image.load('pipe-red.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

                self.rect = self.image.get_rect()
                self.rect[0] = xpos

                if inverted:
                    self.image = pygame.transform.flip(self.image, False, True)
                    self.rect[1] = - (self.rect[3] - ysize)
                else:
                    self.rect[1] = SCREEN_HEIGHT - ysize

                self.mask = pygame.mask.from_surface(self.image)

            def update(self):
                self.rect[0] -= GAME_SPEED

        class Ground(pygame.sprite.Sprite):

            def __init__(self, xpos):
                pygame.sprite.Sprite.__init__(self)

                self.image = pygame.image.load('base.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

                self.mask = pygame.mask.from_surface(self.image)

                self.rect = self.image.get_rect()
                self.rect[0] = xpos
                self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        
            def update(self):
                self.rect[0] -= GAME_SPEED

        def is_off_screen(sprite):
            return sprite.rect[0] < -(sprite.rect[2])

        def get_random_pipes(xpos):
            size = random.randint(100, 300)
            pipe = Pipe(False, xpos, size)
            pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
            return (pipe, pipe_inverted)


        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        start_time = pygame.time.get_ticks()


        BACKGROUND = pygame.image.load('background-day.png')
        BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

        bird_group = pygame.sprite.Group()
        bird = Bird()
        bird_group.add(bird)

        ground_group = pygame.sprite.Group()
        for i in range(2):
            ground = Ground(GROUND_WIDTH * i)
            ground_group.add(ground)

        pipe_group = pygame.sprite.Group()
        for i in range(2):
            pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])


        clock = pygame.time.Clock()

        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        bird.bump()
                        
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

            screen.blit(BACKGROUND, (0, 0))

            font = pygame.font.Font(None, 36)
            text = font.render("Tempo: {:.2f}s".format(elapsed_time), True, (255, 255, 255))
            screen.blit(text, (10, 10))

            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])

                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])
                pipe_group.remove(pipe_group.sprites()[0])

                pipes = get_random_pipes(SCREEN_WIDTH * 2)

                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])

            bird_group.update()
            ground_group.update()
            pipe_group.update()

            bird_group.draw(screen)
            pipe_group.draw(screen)
            ground_group.draw(screen)

            pygame.display.update()

            if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                # Game over
                pygame.quit()
     

    def jogar_velha(self):

        #cores
        co0 = '#FFFFFF' #branco
        co1 = '#333333' #preto pesado
        co2 = '#fcc058' #laranja
        co3 = '#38576b' #valor
        co4 = '#3297a8' #azul
        co5 = '#fff873' #amarelo
        co6 = '#fcc058' #laranja
        co7 = '#e85151' #vermelho
        co8 = '#3297a8' #azul
        co10 = '#fcfbf7' 
        fundo = '#3b3b3b' #preto

        #criando janela principal
        janela = Tk()
        janela.title('Jogo da Velha')

        janela.geometry('260x370')
        janela.configure(bg=fundo)

        #Dividindo a janela em frames
        frame_cima = Frame(janela, width=240, height=100, bg=co1, relief='raised')
        frame_cima.grid(row=0, column=0, sticky=NW, pady=10, padx=10)

        frame_baixo = Frame(janela, width=240, height=300, bg=fundo, relief='flat')
        frame_baixo.grid(row=1, column=0, sticky=NW)

        #Configurando frame cima
        app_x = Label(frame_cima, text='X', height=1, relief='flat', anchor='center', font=('Ivy 40 bold'), bg=co1, fg=co7)
        app_x.place(x=25, y=10)
        app_x = Label(frame_cima, text='Jogador 1 ', height=1, relief='flat', anchor='center', font=('Ivy 7 bold'), bg=co1, fg=co0)
        app_x.place(x=17, y=70)
        app_x_pontos = Label(frame_cima, text='0', height=1, relief='flat', anchor='center', font=('Ivy 30 bold'), bg=co1, fg=co0)
        app_x_pontos.place(x=80, y=20)

        app_separador = Label(frame_cima, text=':', height=1, relief='flat', anchor='center', font=('Ivy 30 bold'), bg=co1, fg=co0)
        app_separador.place(x=110, y=20)

        app_0 = Label(frame_cima, text='O', height=1, relief='flat', anchor='center', font=('Ivy 40 bold'), bg=co1, fg=co4)
        app_0.place(x=170, y=10)
        app_0 = Label(frame_cima, text='Jogador 2', height=1, relief='flat', anchor='center', font=('Ivy 7 bold'), bg=co1, fg=co0)
        app_0.place(x=165, y=70)
        app_0_pontos = Label(frame_cima, text='0', height=1, relief='flat', anchor='center', font=('Ivy 30 bold'), bg=co1, fg=co0)
        app_0_pontos.place(x=130, y=20)


        #Criando lógica do app


        tabela = [['1','2','3'], ['4','5','6'], ['7','8','9']]



        def iniciar_jogo():
            b_jogar.place(x=800, y=350)
            #para controlar o jogo
            def controlar(i):
                global jogando
                global contador
                global jogar 


                #comparando o valor recebido
                if i==str(1):
                    #verificando se a aquela posição está vazia
                    if b_0['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_0['fg'] = cor
                        b_0['text'] = jogando
                        tabela[0][0] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1              

                if i==str(2):
                    #verificando se a aquela posição está vazia
                    if b_1['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_1['fg'] = cor
                        b_1['text'] = jogando
                        tabela[0][1] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                if i==str(3):
                    #verificando se a aquela posição está vazia
                    if b_2['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_2['fg'] = cor
                        b_2['text'] = jogando
                        tabela[0][2] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                if i==str(4):

                    #verificando se a aquela posição está vazia
                    if b_3['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_3['fg'] = cor
                        b_3['text'] = jogando
                        tabela[1][0] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                if i==str(5):
                    #verificando se a aquela posição está vazia
                    if b_4['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_4['fg'] = cor
                        b_4['text'] = jogando
                        tabela[1][1] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                if i==str(6):
                    #verificando se a aquela posição está vazia
                    if b_5['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_5['fg'] = cor
                        b_5['text'] = jogando
                        tabela[1][2] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                if i==str(7):
                    #verificando se a aquela posição está vazia
                    if b_6['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_6['fg'] = cor
                        b_6['text'] = jogando
                        tabela[2][0] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                if i==str(8):
                    #verificando se a aquela posição está vazia
                    if b_7['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_7['fg'] = cor
                        b_7['text'] = jogando
                        tabela[2][1] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                if i==str(9):
                    #verificando se a aquela posição está vazia
                    if b_8['text']=='':             

                        #verificando quem esta a jogar e assim definir a cor do simbolo
                        if jogando =='X':
                            cor=co7
                        if jogando =='O':
                            cor=co8

                        #definir cor do texto do botão e marcar a posição da tabela com o valor do jogador atual
                        b_8['fg'] = cor
                        b_8['text'] = jogando
                        tabela[2][2] = jogando

                        #verificando quem esta jogando para poder trocar o jogador
                        if jogando == 'X':
                            jogando = 'O'
                            joga = 'Jogador 1'
                        else: 
                            jogando = 'X'
                            joga = 'Jogador 2'

                        #incrementar contador para proxima rodada
                        contador += 1

                #apos o contador ser maior ou igual a 5, verifica se houve algum vencedor de acordo com os padrões:
                if contador >= 5:
                    #linhas
                    if tabela[0][0]==tabela[0][1]==tabela[0][2] != '':
                                vencedor(jogando)
                    elif tabela[1][0]==tabela[1][1]==tabela[1][2] != '':
                                vencedor(jogando)
                    elif tabela[2][0]==tabela[2][1]==tabela[2][2] != '':
                                vencedor(jogando)
                            #colunas
                    if tabela[0][0]==tabela[1][0]==tabela[2][0] != '':
                                vencedor(jogando)
                    elif tabela[0][1]==tabela[1][1]==tabela[2][1] != '':
                                vencedor(jogando)
                    elif tabela[0][2]==tabela[1][2]==tabela[2][2] != '':
                                vencedor(jogando)
                            #diagonal
                    if tabela[0][0]==tabela[1][1]==tabela[2][2] != '':
                                vencedor(jogando)
                    elif tabela[0][2]==tabela[1][1]==tabela[2][0] != '':
                                vencedor(jogando)
                            #empate
                    if contador >= 9:
                                vencedor('Empate')        



            #para decidir o vencedor 
            def vencedor(i):
                global contador
                global contador_rodada 
                global tabela         
                global score_1
                global score_2

                #limpando  botões
                b_0['text'] = ''
                b_1['text'] = ''
                b_2['text'] = ''
                b_3['text'] = ''
                b_4['text'] = ''
                b_5['text'] = ''
                b_6['text'] = ''
                b_7['text'] = ''
                b_8['text'] = ''

                b_0['state'] = 'disable'
                b_1['state'] = 'disable'
                b_2['state'] = 'disable'
                b_3['state'] = 'disable'
                b_4['state'] = 'disable'
                b_6['state'] = 'disable'
                b_7['state'] = 'disable'
                b_8['state'] = 'disable'

                app_vencedor = Label(frame_baixo, text='', width=17, relief='flat', anchor='center', font=('Ivy 13 bold'), bg=co2, fg=co0)
                app_vencedor.place(x=40, y=220)

                if i == 'X':
                    score_2 += 1
                    app_vencedor['text'] = 'Jogador 2 venceu'
                    app_0_pontos['text'] = score_2

                if i == 'O':
                    score_1 += 1
                    app_vencedor['text'] = 'Jogador 1 venceu'
                    app_x_pontos['text'] = score_1

                if i == 'Empate':
                    app_vencedor['text'] = 'Empate'

                def start():

                    b_0['text'] = ''
                    b_1['text'] = ''
                    b_2['text'] = ''
                    b_3['text'] = ''
                    b_4['text'] = ''
                    b_5['text'] = ''
                    b_6['text'] = ''
                    b_7['text'] = ''
                    b_8['text'] = ''


                    b_0['state'] = 'normal'
                    b_1['state'] = 'normal'
                    b_2['state'] = 'normal'
                    b_3['state'] = 'normal'
                    b_4['state'] = 'normal'
                    b_6['state'] = 'normal'
                    b_7['state'] = 'normal'
                    b_8['state'] = 'normal'

                    app_vencedor.destroy()
                    b_jogar.destroy()

                b_jogar = Button(frame_baixo, command=start, text='Próxima rodada',height=1, font=('Ivy 10 bold'), overrelief=RIDGE,relief='raised', bg=fundo, fg=co0)
                b_jogar.place(x=70, y=197)

                def jogo_acabou():
                    b_jogar.destroy()
                    app_vencedor.destroy()

                    terminar()

                if contador_rodada >= 3 :
                    jogo_acabou()
                else:
                    contador_rodada += 1
                    #reiniciando a tabela 
                    tabela = [['1','2','3'], ['4','5','6'], ['7','8','9']]
                    contador = 0 




            #para terminar o jogo atual
            def terminar():
                global tabela
                global contador_rodada
                global score_1
                global score_2
                global contador

                tabela = [['1','2','3'], ['4','5','6'], ['7','8','9']]
                contador_rodada = 0
                score_1 = 0
                score_2 = 0
                contador = 0                                                        

                #bloqueando botões
                b_0['state'] = 'disable'
                b_1['state'] = 'disable'
                b_2['state'] = 'disable'
                b_3['state'] = 'disable'
                b_4['state'] = 'disable'
                b_6['state'] = 'disable'
                b_7['state'] = 'disable'
                b_8['state'] = 'disable'

                app_fim = Label(frame_baixo, text='GAME OVER', width=14, relief='flat', anchor='center', font=('Ivy 13 bold'), bg=co2, fg=co0)
                app_fim.place(x=35, y=90)

                # jogar de novo

                def jogar_novamente():
                    app_x_pontos['text'] = '0'
                    app_0_pontos['text'] = '0'
                    app_fim.destroy()
                    b_jogar.destroy()

                    #chamando função iniciar jogo
                    iniciar_jogo()


                #botão jogar novamente
                b_jogar = Button(frame_baixo, command=jogar_novamente, text='Jogar novamente', height=1, font=('Ivy 10 bold'), overrelief=RIDGE,relief='raised', bg=fundo, fg=co0)
                b_jogar.place(x=45, y=197)
                
                def sair():
                    janela.quit()

                b_sair = Button(frame_baixo, command=sair, text='Sair', height=1, font=('Ivy 10 bold'), overrelief=RIDGE,relief='raised', bg=fundo, fg=co0)
                b_sair.place(x=178, y=197)     

            #Configurando frame baixo
            #Linhas verticais
            app_ = Label(frame_baixo, text='', height=23, relief='flat', pady=5, anchor='center', font=('Ivy 5 bold'), bg=co0, fg=co7)
            app_.place(x=90, y=15)
            app_ = Label(frame_baixo, text='', height=23, relief='flat', pady=5, anchor='center', font=('Ivy 5 bold'), bg=co0, fg=co7)
            app_.place(x=157, y=15)

            #Linhas horizontais 
            app_ = Label(frame_baixo, text='', width=46, relief='flat', padx=2, pady=1, anchor='center', font=('Ivy 5 bold'), bg=co0, fg=co7)
            app_.place(x=30, y=63)
            app_ = Label(frame_baixo, text='', width=46, relief='flat', padx=2, pady=1, anchor='center', font=('Ivy 5 bold'), bg=co0, fg=co7)
            app_.place(x=30, y=127)

            #Linha 0
            b_0 = Button(frame_baixo, command=lambda:controlar('1'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_0.place(x=30, y=15)
            b_1 = Button(frame_baixo,command=lambda:controlar('2'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_1.place(x=96, y=15)
            b_2 = Button(frame_baixo,command=lambda:controlar('3'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_2.place(x=163, y=15)

            #Linha 1
            b_3 = Button(frame_baixo,command=lambda:controlar('4'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_3.place(x=30, y=75)
            b_4 = Button(frame_baixo,command=lambda:controlar('5'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_4.place(x=96, y=75)
            b_5 = Button(frame_baixo,command=lambda:controlar('6'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_5.place(x=163, y=75)

            #Linha 2
            b_6 = Button(frame_baixo,command=lambda:controlar('7'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_6.place(x=30, y=135)
            b_7 = Button(frame_baixo,command=lambda:controlar('8'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_7.place(x=96, y=135)
            b_8 = Button(frame_baixo,command=lambda:controlar('9'), text='', width=3, height=1, font=('Ivy 20 bold'), overrelief=RIDGE,relief='flat', bg=fundo, fg=co7)
            b_8.place(x=163, y=135)

        #Botão jogar
        #Linha 1
        b_jogar = Button(frame_baixo, command=iniciar_jogo, text='Jogar', width=10, height=1, font=('Ivy 10 bold'), overrelief=RIDGE,relief='raised', bg=fundo, fg=co0)
        b_jogar.place(x=80, y=210)


        janela.mainloop()



    def jogar_cobrinha(self):
        # Aqui você coloca o código do jogo da cobrinha
        pygame.init()
        font_style = pygame.font.SysFont(None, 50)

        white = (255, 255, 255)
        yellow = (255, 255, 102)
        black = (0, 0, 0)
        red = (213, 50, 80)
        green = (0, 255, 0)
        blue = (50, 153, 213)

        dis_width = 800
        dis_height = 600
        dis = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('Jogo da Cobrinha')

        clock = pygame.time.Clock()

        snake_block = 10
        snake_speed = 30

        def message(msg, color):
            mesg = font_style.render(msg, True, color)
            dis.blit(mesg, [dis_width / 6, dis_height / 3])

        game_over = False
        game_close = False

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        while not game_over:

            while game_close == True:
                dis.fill(blue)
                message("Q-Sair ou C-Jogar Novamente", red)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            for segment in snake_List:
                pygame.draw.rect(dis, black, [segment[0], segment[1], snake_block, snake_block])

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1

            clock.tick(snake_speed)

        pygame.quit()
        quit()

if __name__ == "__main__":
    app = MenuJogos()
    app.mainloop()
