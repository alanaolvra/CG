import pygame
import random
import sys

def jogo_cobrinha():
    pygame.init()

    # Configurações
    largura, altura = 600, 400
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jogo da Cobrinha")

    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 25)

    # Cores
    PRETO = (0, 0, 0)
    VERDE = (0, 255, 0)
    VERMELHO = (255, 0, 0)
    BRANCO = (255, 255, 255)

    # Cobrinha
    tamanho_bloco = 20
    velocidade = 15

    def desenhar_cobrinha(blocos):
        for bloco in blocos:
            pygame.draw.rect(tela, VERDE, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

    def mostrar_pontuacao(pontos):
        texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)
        tela.blit(texto, [10, 10])

    def fim_de_jogo():
        msg = fonte.render("Fim de jogo! Pressione qualquer tecla para sair...", True, VERMELHO)
        tela.blit(msg, [largura // 6, altura // 2])
        pygame.display.update()
        esperar_tecla()

    def esperar_tecla():
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    return

    # Loop principal
    def loop_jogo():
        x = largura // 2
        y = altura // 2
        x_mudanca = 0
        y_mudanca = 0

        cobrinha = []
        comprimento = 1

        comida_x = round(random.randrange(0, largura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
        comida_y = round(random.randrange(0, altura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco

        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT and x_mudanca == 0:
                        x_mudanca = -tamanho_bloco
                        y_mudanca = 0
                    elif evento.key == pygame.K_RIGHT and x_mudanca == 0:
                        x_mudanca = tamanho_bloco
                        y_mudanca = 0
                    elif evento.key == pygame.K_UP and y_mudanca == 0:
                        y_mudanca = -tamanho_bloco
                        x_mudanca = 0
                    elif evento.key == pygame.K_DOWN and y_mudanca == 0:
                        y_mudanca = tamanho_bloco
                        x_mudanca = 0

            x += x_mudanca
            y += y_mudanca

            if x < 0 or x >= largura or y < 0 or y >= altura:
                fim_de_jogo()
                return

            tela.fill(PRETO)
            pygame.draw.rect(tela, VERMELHO, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])

            cabeça = [x, y]
            cobrinha.append(cabeça)
            if len(cobrinha) > comprimento:
                del cobrinha[0]

            for bloco in cobrinha[:-1]:
                if bloco == cabeça:
                    fim_de_jogo()
                    return

            desenhar_cobrinha(cobrinha)
            mostrar_pontuacao(comprimento - 1)
            pygame.display.update()

            if x == comida_x and y == comida_y:
                comida_x = round(random.randrange(0, largura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
                comida_y = round(random.randrange(0, altura - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
                comprimento += 1

            clock.tick(velocidade)

    loop_jogo()
    pygame.quit()