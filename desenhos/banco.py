from OpenGL.GL import *

banco_display_list = None
def configurar_iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 5.0, 2.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 50)

def desenhar_retangulo_escalado(x, y, z, sx, sy, sz, usar_textura=False, textura=None):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    
    if usar_textura and textura:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura)
        glColor3f(1, 1, 1)
        desenhar_retangulo(repeat_x=sx, repeat_y=sz)
        glDisable(GL_TEXTURE_2D)
    else:
        glColor3f(0.1, 0.1, 0.1)
        desenhar_retangulo()

    glPopMatrix()

def desenhar_retangulo(repeat_x=4, repeat_y=4):
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
    global banco_display_list
    if banco_display_list is None:
        banco_display_list = glGenLists(1)
        glNewList(banco_display_list, GL_COMPILE)

        comprimento_ripa = 8
        altura_assento = 0.4
        espessura = 0.08
        profundidade = 0.20
        altura_encosto = 0.7
        largura_total = comprimento_ripa
        offset_perna = largura_total / 2 - 0.1

        if textura_madeira:
            # Assento
            desenhar_retangulo_escalado(0, altura_assento, -0.12, comprimento_ripa, espessura, profundidade, True, textura_madeira)
            desenhar_retangulo_escalado(0, altura_assento,  0.12, comprimento_ripa, espessura, profundidade, True, textura_madeira)

            # Encosto
            glPushMatrix()
            glTranslatef(0, altura_encosto, -0.25)
            glRotatef(90, 1, 0, 0)
            desenhar_retangulo_escalado(0, 0, 0, comprimento_ripa, espessura, profundidade, True, textura_madeira)
            glPopMatrix()
        else:
            glColor3f(0.5, 0.3, 0.1)

        # Suportes
        glColor3f(0.1, 0.1, 0.1)
        for suporte_x in [-offset_perna, offset_perna]:
            desenhar_retangulo_escalado(suporte_x, altura_assento / 2, 0.12, 0.05, altura_assento, 0.05)
            desenhar_retangulo_escalado(suporte_x, altura_encosto / 2, -0.25, 0.05, altura_encosto, 0.05)

        glEndList()

    glPushMatrix()
    glTranslatef(pos_x, 0, 0)
    glCallList(banco_display_list)
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
