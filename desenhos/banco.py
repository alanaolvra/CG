from OpenGL.GL import *

def desenhar_cubo_escalado(x, y, z, sx, sy, sz):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    desenhar_cubo_unitario()
    glPopMatrix()

def desenhar_cubo_unitario():
    glBegin(GL_QUADS)
    # Frente
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    # Trás
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    # Esquerda
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    # Direita
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5,  0.5, -0.5)
    glVertex3f(0.5,  0.5,  0.5)
    glVertex3f(0.5, -0.5,  0.5)
    # Topo
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5,  0.5)
    glVertex3f( 0.5, 0.5,  0.5)
    glVertex3f( 0.5, 0.5, -0.5)
    # Base
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f(-0.5, -0.5,  0.5)
    glEnd()

def desenhar_banco_modular(pos_x=0):
    glPushMatrix()
    glTranslatef(pos_x, 0, 0)
    comprimento_ripa = 8
    altura_assento = 0.4
    espessura = 0.08
    profundidade = 0.20

    # === Madeira ===
    glColor3f(0.5, 0.3, 0.1)

    # Assento (2 ripas horizontais)
    desenhar_cubo_escalado(0, altura_assento, -0.12, comprimento_ripa, espessura, profundidade)
    desenhar_cubo_escalado(0, altura_assento,  0.12, comprimento_ripa, espessura, profundidade)

    # Encosto (ripa única horizontal, no topo das hastes traseiras)
    altura_encosto = 0.7
    glPushMatrix()
    glTranslatef(0, altura_encosto, -0.25)
    glRotatef(90, 1, 0, 0)  # Rotaciona 90° ao redor do eixo Z
    desenhar_cubo_escalado(0, 0, 0, comprimento_ripa, espessura, profundidade)
    glPopMatrix()

    # === Suportes metálicos (pretos)
    glColor3f(0.1, 0.1, 0.1)

    largura_total = comprimento_ripa
    offset_perna = largura_total / 2 - 0.1  # margem de 0.1

    # Pernas da frente (sustentam o assento)
    for suporte_x in [-offset_perna, offset_perna]:
        desenhar_cubo_escalado(suporte_x, altura_assento / 2, 0.12, 0.05, altura_assento, 0.05)

    # Hastes traseiras (vão do chão até o encosto, passando por trás do assento)
    for suporte_x in [-offset_perna, offset_perna]:
        altura_total_haste = altura_encosto
        centro_haste = altura_total_haste / 2
        desenhar_cubo_escalado(suporte_x, centro_haste, -0.25, 0.05, altura_total_haste, 0.05)
    glPopMatrix()

def desenhar_bancos(lado, distancia=4.28):
    glPushMatrix()
    glTranslatef(lado, 0, 0)

    # Banco 1 - atrás, virado para centro (frente → direita)
    glPushMatrix()
    glTranslatef(0, 0, distancia)
    glRotatef(0, 0, 1, 0)
    desenhar_banco_modular()
    glPopMatrix()

    # Banco 2 - direita, virado para centro (esquerda)
    glPushMatrix()
    glTranslatef(-distancia, 0, 0)
    glRotatef(-90, 0, 1, 0)
    desenhar_banco_modular()
    glPopMatrix()

    # Banco 3 - frente, virado para centro (trás → esquerda)
    glPushMatrix()
    glTranslatef(0, 0, -distancia)
    glRotatef(180, 0, 1, 0)
    desenhar_banco_modular()
    glPopMatrix()

    # Banco 4 - esquerda, virado para centro (direita)
    glPushMatrix()
    glTranslatef(distancia, 0, 0)
    glRotatef(90, 0, 1, 0)
    desenhar_banco_modular()
    glPopMatrix()

    glPopMatrix()