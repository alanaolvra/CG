from OpenGL.GL import *
import math

angulo_horas = 0
angulo_minutos = 0

def desenhar_quadrado(tamanho):
    meio = tamanho / 2
    glBegin(GL_QUADS)
    glVertex3f(-meio, -meio, 0.01)
    glVertex3f(meio, -meio, 0.01)
    glVertex3f(meio, meio, 0.01)
    glVertex3f(-meio, meio, 0.01)
    glEnd()

def desenhar_ponteiro(angulo, comprimento, largura):
    glPushMatrix()
    glRotatef(-angulo, 0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-largura/2, 0, 0.02)
    glVertex3f(largura/2, 0, 0.02)
    glVertex3f(largura/2, comprimento, 0.02)
    glVertex3f(-largura/2, comprimento, 0.02)
    glEnd()
    glPopMatrix()



def desenhar_relogio_face():
    # Borda cinza escuro
    glColor3f(0.2, 0.2, 0.2)

    # Círculo branco do relógio
    glColor3f(1, 1, 1)
    desenhar_quadrado(0.58)

    # Ponteiro das horas
    glColor3f(0, 0, 0)  # Preto
    desenhar_ponteiro(angulo_horas, 0.15, 0.02)

    # Ponteiro dos minutos
    glColor3f(0, 0, 0)  # Preto
    desenhar_ponteiro(angulo_minutos, 0.25, 0.01)



def desenhar_relogio():
    global angulo_horas, angulo_minutos

    # Desenhar relógio nas 4 faces
    faces = [
        (0, 4.0, 0.50, 0),     # Frente
        (0, 4.0, -0.50, 180),  # Trás
        (0.50, 4.0, 0, 90),   # Direita
        (-0.50, 4.0, 0, -90)    # Esquerda
    ]


    for x, y, z, rot in faces:
        glPushMatrix()
        glTranslatef(x, y, z)  # Translação para a posição da face
        glRotatef(rot, 0, 1, 0)  # Rotação para a face
        desenhar_relogio_face()  # Desenha o relógio
        glPopMatrix()

    # Atualizar ângulos dos ponteiros
    angulo_minutos += 0.1
    if angulo_minutos >= 360:
        angulo_minutos = 0
        angulo_horas += 30
    if angulo_horas >= 360:
        angulo_horas = 0