from OpenGL.GL import *

def desenhar_torre():
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    glScalef(1, 5, 1)

    glBegin(GL_QUADS)

    # Definindo a altura do relógio
    y_relogio_baixo = 0.1
    y_relogio_cima = 0.3

    # Laterais Pretas (bordas)
    glColor3f(0.0, 0.0, 0.0)

    # Frente - borda esquerda preta
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.2, -0.5, 0.5)
    glVertex3f(-0.2, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Frente - borda direita preta
    glVertex3f(0.2, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.2, 0.5, 0.5)

    # Trás - borda esquerda preta
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.2, -0.5, -0.5)
    glVertex3f(-0.2, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    # Trás - borda direita preta
    glVertex3f(0.2, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.2, 0.5, -0.5)

    # Lados - bordas pretas
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    # Centro (frente)
    # Parte de baixo - branca
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-0.2, -0.5, 0.5)
    glVertex3f(0.2, -0.5, 0.5)
    glVertex3f(0.2, y_relogio_baixo, 0.5)
    glVertex3f(-0.2, y_relogio_baixo, 0.5)

    # Parte do relógio - preta
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-0.2, y_relogio_baixo, 0.5)
    glVertex3f(0.2, y_relogio_baixo, 0.5)
    glVertex3f(0.2, y_relogio_cima, 0.5)
    glVertex3f(-0.2, y_relogio_cima, 0.5)

    # Parte de cima - branca
    glColor3f(0, 0, 0)
    glVertex3f(-0.2, y_relogio_cima, 0.5)
    glVertex3f(0.2, y_relogio_cima, 0.5)
    glVertex3f(0.2, 0.5, 0.5)
    glVertex3f(-0.2, 0.5, 0.5)

    # Centro (trás)
    # Parte de baixo - branca
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-0.2, -0.5, -0.5)
    glVertex3f(0.2, -0.5, -0.5)
    glVertex3f(0.2, y_relogio_baixo, -0.5)
    glVertex3f(-0.2, y_relogio_baixo, -0.5)

    # Parte do relógio - preta
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-0.2, y_relogio_baixo, -0.5)
    glVertex3f(0.2, y_relogio_baixo, -0.5)
    glVertex3f(0.2, y_relogio_cima, -0.5)
    glVertex3f(-0.2, y_relogio_cima, -0.5)

    # Parte de cima - branca
    glColor3f(0.0, 0.0, 0.0)
    glVertex3f(-0.2, y_relogio_cima, -0.5)
    glVertex3f(0.2, y_relogio_cima, -0.5)
    glVertex3f(0.2, 0.5, -0.5)
    glVertex3f(-0.2, 0.5, -0.5)

    # Centro (lados)
    # Lado esquerdo
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-0.5, -0.5, 0.2)
    glVertex3f(-0.5, -0.5, -0.2)
    glVertex3f(-0.5, y_relogio_baixo, -0.2)
    glVertex3f(-0.5, y_relogio_baixo, 0.2)

    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-0.5, y_relogio_baixo, 0.2)
    glVertex3f(-0.5, y_relogio_baixo, -0.2)
    glVertex3f(-0.5, y_relogio_cima, -0.2)
    glVertex3f(-0.5, y_relogio_cima, 0.2)

    glColor3f(0.0, 0.0, 0.0)
    glVertex3f(-0.5, y_relogio_cima, 0.2)
    glVertex3f(-0.5, y_relogio_cima, -0.2)
    glVertex3f(-0.5, 0.5, -0.2)
    glVertex3f(-0.5, 0.5, 0.2)

    # Lado direito
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0.5, -0.5, 0.2)
    glVertex3f(0.5, -0.5, -0.2)
    glVertex3f(0.5, y_relogio_baixo, -0.2)
    glVertex3f(0.5, y_relogio_baixo, 0.2)

    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0.5, y_relogio_baixo, 0.2)
    glVertex3f(0.5, y_relogio_baixo, -0.2)
    glVertex3f(0.5, y_relogio_cima, -0.2)
    glVertex3f(0.5, y_relogio_cima, 0.2)

    glColor3f(0.0, 0.0, 0.0)
    glVertex3f(0.5, y_relogio_cima, 0.2)
    glVertex3f(0.5, y_relogio_cima, -0.2)
    glVertex3f(0.5, 0.5, -0.2)
    glVertex3f(0.5, 0.5, 0.2)

    # Topo preto
    glColor3f(0.0, 0.0, 0.0)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # Base preta
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glEnd()
    glPopMatrix()
