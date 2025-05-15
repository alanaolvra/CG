from OpenGL.GL import *

def desenhar_chao(textura_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(0.9, 0.9, 0.9)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-20, 0, -20)
    glTexCoord2f(20, 0); glVertex3f(20, 0, -20)
    glTexCoord2f(20, 20); glVertex3f(20, 0, 20)
    glTexCoord2f(0, 20); glVertex3f(-20, 0, 20)
    glEnd()

    glDisable(GL_TEXTURE_2D)
