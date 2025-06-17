from OpenGL.GL import *
from colisao import objetos_colisao, transformar_bounding_box

torre_display_list = None

def carregar_torre():
    # Bounding box base: um pouco maior nas laterais e no topo
    bbox_torre_base = {
        "min": [-1.4, -1.4, -1.4],
        "max": [1.4,1.4,1.4]
    }
    escala = [1, 5, 1]
    translacao = [0, 2.5, 0]

    # Aplica transformação na bounding box
    bbox_torre = transformar_bounding_box(bbox_torre_base, escala, translacao)

    # Registra a torre no sistema de colisão
    objetos_colisao["Torre"] = bbox_torre

def desenhar_torre():
    carregar_torre()
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    glScalef(1, 5, 1)

    # Partes brancas
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.8, 0.8)

    y_relogio_baixo = 0.1
    y_relogio_cima = 0.2

    # Frente
    glVertex3f(-0.3, -0.5, 0.5)
    glVertex3f(0.3, -0.5, 0.5)
    glVertex3f(0.3, y_relogio_baixo, 0.5)
    glVertex3f(-0.3, y_relogio_baixo, 0.5)

    glVertex3f(-0.3, y_relogio_baixo, 0.5)
    glVertex3f(0.3, y_relogio_baixo, 0.5)
    glVertex3f(0.3, y_relogio_cima, 0.5)
    glVertex3f(-0.3, y_relogio_cima, 0.5)

    # Trás
    glVertex3f(-0.3, -0.5, -0.5)
    glVertex3f(0.3, -0.5, -0.5)
    glVertex3f(0.3, y_relogio_baixo, -0.5)
    glVertex3f(-0.3, y_relogio_baixo, -0.5)

    glVertex3f(-0.3, y_relogio_baixo, -0.5)
    glVertex3f(0.3, y_relogio_baixo, -0.5)
    glVertex3f(0.3, y_relogio_cima, -0.5)
    glVertex3f(-0.3, y_relogio_cima, -0.5)

    # Lados
    glVertex3f(-0.5, -0.5, 0.3)
    glVertex3f(-0.5, -0.5, -0.3)
    glVertex3f(-0.5, y_relogio_baixo, -0.3)
    glVertex3f(-0.5, y_relogio_baixo, 0.3)

    glVertex3f(-0.5, y_relogio_baixo, 0.3)
    glVertex3f(-0.5, y_relogio_baixo, -0.3)
    glVertex3f(-0.5, y_relogio_cima, -0.3)
    glVertex3f(-0.5, y_relogio_cima, 0.3)

    glVertex3f(0.5, -0.5, 0.3)
    glVertex3f(0.5, -0.5, -0.3)
    glVertex3f(0.5, y_relogio_baixo, -0.3)
    glVertex3f(0.5, y_relogio_baixo, 0.3)

    glVertex3f(0.5, y_relogio_baixo, 0.3)
    glVertex3f(0.5, y_relogio_baixo, -0.3)
    glVertex3f(0.5, y_relogio_cima, -0.3)
    glVertex3f(0.5, y_relogio_cima, 0.3)
    glEnd()

    # Partes pretas
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.0)

    # Bordas frente
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.3, -0.5, 0.5)
    glVertex3f(-0.3, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    glVertex3f(0.3, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.3, 0.5, 0.5)

    # Bordas trás
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.3, -0.5, -0.5)
    glVertex3f(-0.3, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    glVertex3f(0.3, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.3, 0.5, -0.5)

    # Laterais pretas
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

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

    # Parte de cima da frente
    glVertex3f(-0.3, y_relogio_cima, 0.5)
    glVertex3f(0.3, y_relogio_cima, 0.5)
    glVertex3f(0.3, 0.5, 0.5)
    glVertex3f(-0.3, 0.5, 0.5)

    # Parte de cima de trás
    glVertex3f(-0.3, y_relogio_cima, -0.5)
    glVertex3f(0.3, y_relogio_cima, -0.5)
    glVertex3f(0.3, 0.5, -0.5)
    glVertex3f(-0.3, 0.5, -0.5)

    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)
    glPopMatrix()
