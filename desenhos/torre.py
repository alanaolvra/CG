from OpenGL.GL import *

def desenhar_torre():
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    glScalef(1, 5, 1)

    glBegin(GL_QUADS)

    # Definindo a altura do relógio
    y_relogio_baixo = 0.1
    y_relogio_cima = 0.3

    # PARTES BRANCAS (DESENHADAS PRIMEIRO)
    glColor3f(1.0, 1.0, 1.0)

    # FRENTE
    # Parte de baixo branca (frente)
    glVertex3f(-0.2, -0.5, 0.5)
    glVertex3f(0.2, -0.5, 0.5)
    glVertex3f(0.2, y_relogio_baixo, 0.5)
    glVertex3f(-0.2, y_relogio_baixo, 0.5)

    # Parte do relógio branca (frente)
    glVertex3f(-0.2, y_relogio_baixo, 0.5)
    glVertex3f(0.2, y_relogio_baixo, 0.5)
    glVertex3f(0.2, y_relogio_cima, 0.5)
    glVertex3f(-0.2, y_relogio_cima, 0.5)

    # TRÁS
    # Parte de baixo branca (trás)
    glVertex3f(-0.2, -0.5, -0.5)
    glVertex3f(0.2, -0.5, -0.5)
    glVertex3f(0.2, y_relogio_baixo, -0.5)
    glVertex3f(-0.2, y_relogio_baixo, -0.5)

    # Parte do relógio branca (trás)
    glVertex3f(-0.2, y_relogio_baixo, -0.5)
    glVertex3f(0.2, y_relogio_baixo, -0.5)
    glVertex3f(0.2, y_relogio_cima, -0.5)
    glVertex3f(-0.2, y_relogio_cima, -0.5)

    # LADOS
    # Lado esquerdo (branco)
    glVertex3f(-0.5, -0.5, 0.2)
    glVertex3f(-0.5, -0.5, -0.2)
    glVertex3f(-0.5, y_relogio_baixo, -0.2)
    glVertex3f(-0.5, y_relogio_baixo, 0.2)

    glVertex3f(-0.5, y_relogio_baixo, 0.2)
    glVertex3f(-0.5, y_relogio_baixo, -0.2)
    glVertex3f(-0.5, y_relogio_cima, -0.2)
    glVertex3f(-0.5, y_relogio_cima, 0.2)

    # Lado direito (branco)
    glVertex3f(0.5, -0.5, 0.2)
    glVertex3f(0.5, -0.5, -0.2)
    glVertex3f(0.5, y_relogio_baixo, -0.2)
    glVertex3f(0.5, y_relogio_baixo, 0.2)

    glVertex3f(0.5, y_relogio_baixo, 0.2)
    glVertex3f(0.5, y_relogio_baixo, -0.2)
    glVertex3f(0.5, y_relogio_cima, -0.2)
    glVertex3f(0.5, y_relogio_cima, 0.2)

    glEnd()

    # PARTES PRETAS (DESENHADAS DEPOIS)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)  # Ajuste esses valores se necessário
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.0)

    # BORDAS DA FRENTE
    # Borda esquerda (frente)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.2, -0.5, 0.5)
    glVertex3f(-0.2, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Borda direita (frente)
    glVertex3f(0.2, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.2, 0.5, 0.5)

    # BORDAS DE TRÁS
    # Borda esquerda (trás)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.2, -0.5, -0.5)
    glVertex3f(-0.2, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    # Borda direita (trás)
    glVertex3f(0.2, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.2, 0.5, -0.5)

    # LADOS PRETOS
    # Lado direito (borda preta)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    # Lado esquerdo (borda preta)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    # TOPO E BASE PRETOS
    # Topo
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # Base
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    # PARTES PRETAS SUPERIORES (frente/trás)
    # Parte de cima da frente
    glVertex3f(-0.2, y_relogio_cima, 0.5)
    glVertex3f(0.2, y_relogio_cima, 0.5)
    glVertex3f(0.2, 0.5, 0.5)
    glVertex3f(-0.2, 0.5, 0.5)

    # Parte de cima de trás
    glVertex3f(-0.2, y_relogio_cima, -0.5)
    glVertex3f(0.2, y_relogio_cima, -0.5)
    glVertex3f(0.2, 0.5, -0.5)
    glVertex3f(-0.2, 0.5, -0.5)

    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)
    glPopMatrix()