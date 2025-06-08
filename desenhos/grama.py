from OpenGL.GL import *

def desenhar_grama(lado, textura_grama, repeat=10):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_grama)
    glColor3f(1.0, 1.0, 1.0)

    grama = 8  # tamanho do quadrado
    y = 0.01  # levemente acima do chão

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

