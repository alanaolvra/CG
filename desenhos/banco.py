from OpenGL.GL import *

def configurar_iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Posição da luz
    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 5.0, 2.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # Propriedades do material
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 50)

def desenhar_cubo_escalado(x, y, z, sx, sy, sz, usar_textura=False, textura=None):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    
    if usar_textura and textura:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura)
        glColor3f(1, 1, 1)  # Mantém cor branca para não interferir na textura
        desenhar_cubo_unitario(repeat_x=sx, repeat_y=sz)
        glDisable(GL_TEXTURE_2D)
    else:
        glColor3f(0.1, 0.1, 0.1)
        desenhar_cubo_unitario()

    glPopMatrix()

def desenhar_cubo_unitario(repeat_x=4, repeat_y=4):
    glBegin(GL_QUADS)

    # Frente
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5,  0.5)
    glTexCoord2f(repeat_x, 0); glVertex3f( 0.5, -0.5,  0.5)
    glTexCoord2f(repeat_x, repeat_y); glVertex3f( 0.5,  0.5,  0.5)
    glTexCoord2f(0, repeat_y); glVertex3f(-0.5,  0.5,  0.5)

    # Trás
    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(repeat_x, 0); glVertex3f( 0.5, -0.5, -0.5)
    glTexCoord2f(repeat_x, repeat_y); glVertex3f( 0.5,  0.5, -0.5)
    glTexCoord2f(0, repeat_y); glVertex3f(-0.5,  0.5, -0.5)

    # Esquerda
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(repeat_x, 0); glVertex3f(-0.5, -0.5,  0.5)
    glTexCoord2f(repeat_x, repeat_y); glVertex3f(-0.5,  0.5,  0.5)
    glTexCoord2f(0, repeat_y); glVertex3f(-0.5,  0.5, -0.5)

    # Direita
    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(repeat_x, 0); glVertex3f(0.5, -0.5,  0.5)
    glTexCoord2f(repeat_x, repeat_y); glVertex3f(0.5,  0.5,  0.5)
    glTexCoord2f(0, repeat_y); glVertex3f(0.5,  0.5, -0.5)

    # Topo
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0); glVertex3f(-0.5, 0.5, -0.5)
    glTexCoord2f(repeat_x, 0); glVertex3f( 0.5, 0.5, -0.5)
    glTexCoord2f(repeat_x, repeat_y); glVertex3f( 0.5, 0.5,  0.5)
    glTexCoord2f(0, repeat_y); glVertex3f(-0.5, 0.5,  0.5)

    # Base
    glNormal3f(0, -1, 0)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(repeat_x, 0); glVertex3f( 0.5, -0.5, -0.5)
    glTexCoord2f(repeat_x, repeat_y); glVertex3f( 0.5, -0.5,  0.5)
    glTexCoord2f(0, repeat_y); glVertex3f(-0.5, -0.5,  0.5)

    glEnd()

def desenhar_banco_modular(pos_x=0, textura_madeira=None):
    glPushMatrix()
    glTranslatef(pos_x, 0, 0)
    comprimento_ripa = 8
    altura_assento = 0.4
    espessura = 0.08
    profundidade = 0.20

    if textura_madeira:
        # Assento
        desenhar_cubo_escalado(0, altura_assento, -0.12, comprimento_ripa, espessura, profundidade, True, textura_madeira)
        desenhar_cubo_escalado(0, altura_assento,  0.12, comprimento_ripa, espessura, profundidade, True, textura_madeira)

        # Encosto
        altura_encosto = 0.7
        glPushMatrix()
        glTranslatef(0, altura_encosto, -0.25)
        glRotatef(90, 1, 0, 0)
        desenhar_cubo_escalado(0, 0, 0, comprimento_ripa, espessura, profundidade, True, textura_madeira)
        glPopMatrix()
    else:
        glColor3f(0.5, 0.3, 0.1)

    # Suportes
    glColor3f(0.1, 0.1, 0.1)
    largura_total = comprimento_ripa
    offset_perna = largura_total / 2 - 0.1

    for suporte_x in [-offset_perna, offset_perna]:
        desenhar_cubo_escalado(suporte_x, altura_assento / 2, 0.12, 0.05, altura_assento, 0.05)
        desenhar_cubo_escalado(suporte_x, altura_encosto / 2, -0.25, 0.05, altura_encosto, 0.05)

    glPopMatrix()

def desenhar_bancos(lado, textura_madeira=None, distancia=4.28):
    glPushMatrix()
    glTranslatef(lado, 0, 0)

    def banco(x, z, rot):
        glPushMatrix()
        glTranslatef(x, 0, z)
        glRotatef(rot, 0, 1, 0)
        desenhar_banco_modular(0, textura_madeira)
        glPopMatrix()

    banco(0, distancia, 0)
    banco(-distancia, 0, -90)
    banco(0, -distancia, 180)
    banco(distancia, 0, 90)

    glPopMatrix()
