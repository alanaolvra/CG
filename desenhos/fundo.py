from OpenGL.GL import *
import math

def desenhar_teto_esferico(raio=30, stacks=20, slices=40, textura_id=None, altura=15):
    if textura_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura_id)

    for i in range(stacks):
        lat0 = math.pi / 2 * (i / stacks)
        lat1 = math.pi / 2 * ((i + 1) / stacks)

        y0 = math.sin(lat0)
        y1 = math.sin(lat1)
        r0 = math.cos(lat0)
        r1 = math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * (j / slices)
            x = math.cos(lng)
            z = math.sin(lng)

            glNormal3f(-x * r1, y1, -z * r1)
            glTexCoord2f(j / slices, (i + 1) / stacks)
            glVertex3f(x * r1 * raio, altura + y1 * raio, z * r1 * raio)

            glNormal3f(-x * r0, y0, -z * r0)
            glTexCoord2f(j / slices, i / stacks)
            glVertex3f(x * r0 * raio, altura + y0 * raio, z * r0 * raio)
        glEnd()

    glDisable(GL_TEXTURE_2D)


def desenhar_ceu(textura_paredes_id, textura_teto_id, tamanho=20, altura=15):
    glPushMatrix()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
    glEnable(GL_LIGHT0)

    # Luz branca vinda de cima
    light_pos = [0.0, 50.0, 0.0, 1.0]
    light_color = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)

    # Material do céu
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [0, 0, -50, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32)

    x_min = -tamanho
    x_max = tamanho
    z_min = -tamanho 
    z_max = tamanho
    y_min = 0
    y_max = altura

    glBindTexture(GL_TEXTURE_2D, textura_paredes_id)

    # Parede traseira
    glNormal3f(0, 0, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x_min, y_min, z_min)
    glTexCoord2f(1, 0); glVertex3f(x_max, y_min, z_min)
    glTexCoord2f(1, 1); glVertex3f(x_max, y_max, z_min)
    glTexCoord2f(0, 1); glVertex3f(x_min, y_max, z_min)
    glEnd()

    # Parede dianteira
    glNormal3f(0, 0, -1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x_max, y_min, z_max)
    glTexCoord2f(1, 0); glVertex3f(x_min, y_min, z_max)
    glTexCoord2f(1, 1); glVertex3f(x_min, y_max, z_max)
    glTexCoord2f(0, 1); glVertex3f(x_max, y_max, z_max)
    glEnd()

    # Parede esquerda
    glNormal3f(1, 0, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x_min, y_min, z_max)
    glTexCoord2f(1, 0); glVertex3f(x_min, y_min, z_min)
    glTexCoord2f(1, 1); glVertex3f(x_min, y_max, z_min)
    glTexCoord2f(0, 1); glVertex3f(x_min, y_max, z_max)
    glEnd()

    # Parede direita
    glNormal3f(-1, 0, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x_max, y_min, z_min)
    glTexCoord2f(1, 0); glVertex3f(x_max, y_min, z_max)
    glTexCoord2f(1, 1); glVertex3f(x_max, y_max, z_max)
    glTexCoord2f(0, 1); glVertex3f(x_max, y_max, z_min)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textura_teto_id)

    # Teto
    glBindTexture(GL_TEXTURE_2D, textura_teto_id)
    glNormal3f(0, 1, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x_min, y_max, z_min)
    glTexCoord2f(1, 0); glVertex3f(x_max, y_max, z_min)
    glTexCoord2f(1, 1); glVertex3f(x_max, y_max, z_max)
    glTexCoord2f(0, 1); glVertex3f(x_min, y_max, z_max)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glPopMatrix()

