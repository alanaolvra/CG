import glfw
import pygame
from pygame import freetype
from OpenGL.GL import *
import numpy as np

from Agente.extrair import extrair_dados

pos_pessoa = np.array([5.6, 1.5, 10.2], dtype=np.float32)
DISTANCIA_INTERACAO = 1.5

mensagens_dialogo = []  # lista de strings
texto_digitado = ""
dialogo_ativo = False

# Inicializa pygame font uma vez (chame no início do programa)
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)

def estar_perto_da_pessoa(pos_camera, frente_camera):
    direcao = pos_pessoa - pos_camera
    distancia = np.linalg.norm(direcao)
    return distancia <= DISTANCIA_INTERACAO

def iniciar_dialogo():
    global dialogo_ativo, texto_digitado, mostrar_resposta
    dialogo_ativo = True
    texto_digitado = ""
    mostrar_resposta = False

def encerrar_dialogo():
    global dialogo_ativo
    dialogo_ativo = False

def is_dialogo_ativo():
    return dialogo_ativo

def tratar_evento_tecla(window, key, scancode, action, mods):
    global texto_digitado, mensagens_dialogo

    if not dialogo_ativo:
        return

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_ENTER:
            if texto_digitado.strip():
                mensagens_dialogo.append("Você: " + texto_digitado)
                # Simula resposta do vendedor (exemplo)
                resposta_vendedor = extrair_dados(texto_digitado, tipo_prompt="vendedor")
                mensagens_dialogo.append(resposta_vendedor)
                texto_digitado = ""
        elif key == glfw.KEY_BACKSPACE:
            texto_digitado = texto_digitado[:-1]


def tratar_evento_char(window, codepoint):
    global texto_digitado

    if not dialogo_ativo:
        return
    texto_digitado += chr(codepoint)

def desenhar_texto_multilinha(texto, x, y, largura_max, cor=(255,255,255)):
    linhas = renderizar_texto_multilinha(texto, FONT, cor, largura_max)
    for i, linha in enumerate(linhas):
        surf = FONT.render(linha, True, cor)
        texto_data = pygame.image.tostring(surf, "RGBA", True)
        glRasterPos2f(x, y - i * 30)  # 30 é a altura de linha
        glDrawPixels(surf.get_width(), surf.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, texto_data)


def desenhar_texto(texto, x, y, color=(255,255,255)):
    surf = FONT.render(texto, True, color)
    texto_data = pygame.image.tostring(surf, "RGBA", True)
    glRasterPos2f(x, y)
    glDrawPixels(surf.get_width(), surf.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, texto_data)

def renderizar_texto_multilinha(texto, fonte, cor, largura_max):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        largura, _ = fonte.size(teste_linha)
        if largura > largura_max and linha_atual != "":
            surf = fonte.render(linha_atual, True, cor)
            linhas.append(surf)
            linha_atual = palavra + " "
        else:
            linha_atual = teste_linha
    if linha_atual:
        surf = fonte.render(linha_atual, True, cor)
        linhas.append(surf)
    return linhas


import time

# Configuração do scroll suave
scroll_offset = 0
scroll_target = 0
scroll_speed = 500  # pixels por segundo
mensagens_animadas = []

# Quando adicionar nova mensagem:
def adicionar_mensagem(msg):
    mensagens_dialogo.append(msg)
    if len(mensagens_dialogo) > 50:
        mensagens_dialogo.pop(0)

    # Definimos novo alvo de scroll
    calcular_scroll_target()

    # Marcar mensagem para animação de fade-in
    mensagens_animadas.append({'texto': msg, 'start_time': time.time()})

def calcular_scroll_target():
    global scroll_target

    padding = 20
    espacamento_mensagem = 15
    altura_total = 0

    ultimas_mensagens = mensagens_dialogo[-50:]
    for msg in ultimas_mensagens:
        if msg.startswith("Você:"):
            texto = msg[6:].strip()
        else:
            texto = msg
        linhas = renderizar_texto_multilinha(texto, FONT, (255, 255, 255), 600)
        altura_msg = sum(linha.get_height() + 5 for linha in linhas) - 5
        altura_total += altura_msg + espacamento_mensagem + 20

    scroll_target = max(0, altura_total - (400 - 2 * padding))

def atualizar_scroll(dt):
    global scroll_offset
    if scroll_offset < scroll_target:
        scroll_offset += scroll_speed * dt
        if scroll_offset > scroll_target:
            scroll_offset = scroll_target
    elif scroll_offset > scroll_target:
        scroll_offset -= scroll_speed * dt
        if scroll_offset < scroll_target:
            scroll_offset = scroll_target
def desenhar_overlay(dt):
    if not dialogo_ativo:
        return

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1920, 0, 1080, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    # Configurações da caixa de diálogo
    margem_lateral = 100
    margem_inferior = 150
    largura_caixa = 1920 - 2 * margem_lateral
    altura_caixa = 400
    x1 = margem_lateral
    y1 = margem_inferior

    # Fundo da caixa preta
    glColor4f(0, 0, 0, 0.5)
    desenhar_retangulo_arredondado(x1, y1, largura_caixa, altura_caixa, 20)

    padding = 20
    espacamento_mensagem = 15
    altura_disponivel = altura_caixa - 2 * padding - 80  # -80 para nunca tocar a barra de input

    # Prepara mensagens para renderizar
    mensagens_render = []
    altura_total = 0

    for msg in reversed(mensagens_dialogo):  # Começa da última para cima
        if msg.startswith("Você:"):
            cor_fundo = (0.2, 0.4, 1.0)
            alinhamento = 'direita'
            texto = msg[6:].strip()
        else:
            cor_fundo = (0.0, 0.7, 0.3)
            alinhamento = 'esquerda'
            texto = msg

        linhas = renderizar_texto_multilinha(texto, FONT, (255, 255, 255), 600)
        altura_msg = sum(linha.get_height() + 5 for linha in linhas) - 5 + 20

        if altura_total + altura_msg > altura_disponivel:
            break  # não cabe mais
        mensagens_render.insert(0, {
            'linhas': linhas,
            'altura': altura_msg,
            'cor_fundo': cor_fundo,
            'alinhamento': alinhamento
        })
        altura_total += altura_msg + espacamento_mensagem

    # Desenha as mensagens de cima para baixo
    linha_y = y1 + altura_caixa - padding

    for item in mensagens_render:
        altura_total = item['altura']
        if item['alinhamento'] == 'esquerda':
            balao_x = x1 + padding
        else:
            balao_x = x1 + largura_caixa - 600 - 20 - padding

        cor = (*item['cor_fundo'], 0.8)
        desenhar_retangulo_arredondado(balao_x, linha_y - altura_total, 600 + 20, altura_total, 15, cor)

        texto_y = linha_y - altura_total + 10
        for linha in reversed(item['linhas']):
            texto_data = pygame.image.tostring(linha, "RGBA", True)
            glRasterPos2f(balao_x + 10, texto_y)
            glDrawPixels(linha.get_width(), linha.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, texto_data)
            texto_y += linha.get_height() + 5

        linha_y -= altura_total + espacamento_mensagem

    # Campo de entrada
    entrada_texto = "Você: " + texto_digitado
    entrada_linhas = renderizar_texto_multilinha(entrada_texto, FONT, (255, 255, 255), largura_caixa - 2 * padding - 20)
    entrada_altura = sum(linha.get_height() + 5 for linha in entrada_linhas) - 5

    desenhar_retangulo_arredondado(
        x1 + padding,
        y1,
        largura_caixa - 2 * padding,
        entrada_altura + 20,
        15,
        (0.2, 0.4, 1.0, 0.7)
    )

    texto_y = y1 + 10
    for linha in entrada_linhas:
        texto_data = pygame.image.tostring(linha, "RGBA", True)
        glRasterPos2f(x1 + padding + 10, texto_y)
        glDrawPixels(linha.get_width(), linha.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, texto_data)
        texto_y += linha.get_height() + 5

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)





import math

def desenhar_retangulo_arredondado(x, y, largura, altura, raio, cor=(0, 0, 0, 0.7)):
    glColor4f(*cor)
    segmentos = 16

    # centro das curvas
    cx = [x + raio, x + largura - raio]
    cy = [y + raio, y + altura - raio]

    # quadrados centrais
    glBegin(GL_QUADS)
    glVertex2f(x + raio, y)
    glVertex2f(x + largura - raio, y)
    glVertex2f(x + largura - raio, y + altura)
    glVertex2f(x + raio, y + altura)

    glVertex2f(x, y + raio)
    glVertex2f(x, y + altura - raio)
    glVertex2f(x + largura, y + altura - raio)
    glVertex2f(x + largura, y + raio)
    glEnd()

    # cantos arredondados
    for i, (cx_i, cy_i) in enumerate([(cx[0], cy[0]), (cx[1], cy[0]), (cx[1], cy[1]), (cx[0], cy[1])]):
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx_i, cy_i)
        for j in range(segmentos + 1):
            ang = j * math.pi / 2 / segmentos + i * math.pi / 2
            glVertex2f(cx_i + raio * math.cos(ang), cy_i + raio * math.sin(ang))
        glEnd()
