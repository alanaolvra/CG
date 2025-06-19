from OpenGL.GL import *
from colisao import objetos_colisao, calcular_bounding_box, transformar_bounding_box

def desenhar_grama(lado, textura_grama, repeat=10):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_grama)
    glColor3f(1.0, 1.0, 1.0)

    grama = 8  
    y = 0.01

    # ------ Bounding Box da Grama ------
    # Coordenadas mínimas e máximas antes da transformação
    bbox_grama = {
        "min": [-grama / 2, y, -grama / 2],
        "max": [ grama / 2, y,  grama / 2]
    }
    # Aplicar transformação (posição "lado" no X)
    bbox_grama = transformar_bounding_box(bbox_grama, escala=[1.2,1.2,1.2], translacao=[lado,0,0])

    # Registrar a grama no dicionário global
    objetos_colisao[f"Grama_{lado}"] = bbox_grama
    # ------------------------------------

    glPushMatrix()
    glTranslatef(lado, 0, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(0,     0);     glVertex3f(-grama/2, y, -grama/2)
    glTexCoord2f(repeat, 0);    glVertex3f( grama/2, y, -grama/2)
    glTexCoord2f(repeat, repeat); glVertex3f( grama/2, y,  grama/2)
    glTexCoord2f(0,     repeat); glVertex3f(-grama/2, y,  grama/2)
    glEnd()

    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
