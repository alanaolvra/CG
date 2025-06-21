from OpenGL.GL import *

def configurar_iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 50)


def desenhar_agua(textura_agua, repeat=1):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_agua)
    glColor3f(1.0, 1.0, 1.0)

    agua = 4.25 
    y = 0.01

    glPushMatrix()
    configurar_iluminacao()
    glTranslatef(0.06, 0, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(0,     0);     glVertex3f(-agua/2, y, -agua/2)
    glTexCoord2f(repeat, 0);    glVertex3f( agua/2, y, -agua/2)
    glTexCoord2f(repeat, repeat); glVertex3f( agua/2, y,  agua/2)
    glTexCoord2f(0,     repeat); glVertex3f(-agua/2, y,  agua/2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glPopMatrix()