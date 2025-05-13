from OpenGL.GL import *

def desenhar_ceu(tamanho=20, altura=20):
    glPushMatrix()

    glColor3f(0.5, 0.7, 1.0)
    
    x_min = -tamanho
    x_max = tamanho
    z_min = -tamanho
    z_max = tamanho
    y_min = 0
    y_max = altura

    # Parede traseira (z_min)
    glBegin(GL_QUADS)
    glVertex3f(x_min, y_min, z_min)
    glVertex3f(x_max, y_min, z_min)
    glVertex3f(x_max, y_max, z_min)
    glVertex3f(x_min, y_max, z_min)
    glEnd()

    # Parede dianteira (z_max)
    glBegin(GL_QUADS)
    glVertex3f(x_min, y_min, z_max)
    glVertex3f(x_max, y_min, z_max)
    glVertex3f(x_max, y_max, z_max)
    glVertex3f(x_min, y_max, z_max)
    glEnd()

    # Parede esquerda (x_min)
    glBegin(GL_QUADS)
    glVertex3f(x_min, y_min, z_min)
    glVertex3f(x_min, y_min, z_max)
    glVertex3f(x_min, y_max, z_max)
    glVertex3f(x_min, y_max, z_min)
    glEnd()

    # Parede direita (x_max)
    glBegin(GL_QUADS)
    glVertex3f(x_max, y_min, z_min)
    glVertex3f(x_max, y_min, z_max)
    glVertex3f(x_max, y_max, z_max)
    glVertex3f(x_max, y_max, z_min)
    glEnd()

    # Teto
    glBegin(GL_QUADS)
    glVertex3f(x_min, y_max, z_min)
    glVertex3f(x_max, y_max, z_min)
    glVertex3f(x_max, y_max, z_max)
    glVertex3f(x_min, y_max, z_max)
    glEnd()

    glPopMatrix()
