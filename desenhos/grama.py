from OpenGL.GL import *
from colisao import objetos_colisao, calcular_bounding_box, transformar_bounding_box

def configurar_iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 50)


def desenhar_grama(lado, textura_grama, repeat=8):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_grama)
    glColor3f(1.0, 1.0, 1.0)

    grama = 8  
    y = 0.01

    bbox_grama = {
        "min": [-grama / 2, y, -grama / 2],
        "max": [ grama / 2, y,  grama / 2]
    }
    
    bbox_grama = transformar_bounding_box(bbox_grama, escala=[1.2,1.2,1.2], translacao=[lado,0,0])

    objetos_colisao[f"Grama_{lado}"] = bbox_grama
    # ------------------------------------

    glPushMatrix()
    configurar_iluminacao()
    glTranslatef(lado, 0, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(0,     0);     glVertex3f(-grama/2, y, -grama/2)
    glTexCoord2f(repeat, 0);    glVertex3f( grama/2, y, -grama/2)
    glTexCoord2f(repeat, repeat); glVertex3f( grama/2, y,  grama/2)
    glTexCoord2f(0,     repeat); glVertex3f(-grama/2, y,  grama/2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glPopMatrix()