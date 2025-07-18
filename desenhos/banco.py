from OpenGL.GL import *
import numpy as np

banco_display_list = None

def phong_iluminacao(P, cam_pos, normal, mat_amb, mat_diff, mat_spec, mat_shine,
                     luz_pos=np.array([2.0, 5.0, 2.0]),
                     luz_amb=np.array([0.8, 0.8, 0.8]),
                     luz_diff=np.array([0.7, 0.7, 0.7]),
                     luz_spec=np.array([1.0, 1.0, 1.0])):
    
    #Reflexão ambiente
    ambient = luz_amb * mat_amb

    #Reflexão difusa
    L = luz_pos - P
    L = L / np.linalg.norm(L)
    N = normal / np.linalg.norm(normal)
    diff = luz_diff * mat_diff * max(np.dot(L, N), 0.0)

    #Reflexão especular
    V = cam_pos - P
    V = V / np.linalg.norm(V)
    R = 2 * np.dot(N, L) * N - L
    spec = luz_spec * mat_spec * (max(np.dot(V, R), 0.0) ** mat_shine)

    cor = ambient + diff + spec
    return np.clip(cor, 0.0, 1.0)

def desenhar_retangulo_escalado(x, y, z, sx, sy, sz, cam_pos, usar_textura=False, textura=None):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)

    if usar_textura and textura:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura)
        glColor3f(1, 1, 1)
        desenhar_retangulo(cam_pos, repeat_x=sx, repeat_y=sz)
        glDisable(GL_TEXTURE_2D)
    else:
        glColor3f(0.1, 0.1, 0.1)
        desenhar_retangulo(cam_pos)

    glPopMatrix()

def desenhar_retangulo(cam_pos, repeat_x=4, repeat_y=4):
    mat_amb = np.array([0.2, 0.1, 0.1])
    mat_diff = np.array([0.7, 0.4, 0.1])
    mat_spec = np.array([0.3, 0.3, 0.1])
    mat_shine = 50

    def vertex(normal, tex_coord, position):
        P = np.array(position)
        cor = phong_iluminacao(P, cam_pos, normal, mat_amb, mat_diff, mat_spec, mat_shine)
        glColor3fv(cor)
        glTexCoord2f(*tex_coord)
        glVertex3f(*position)

    glBegin(GL_QUADS)

    # Frente
    normal = (0, 0, 1)
    tex = [(0, 0), (repeat_x, 0), (repeat_x, repeat_y), (0, repeat_y)]
    verts = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)]
    for tc, v in zip(tex, verts):
        vertex(normal, tc, v)

    # Trás
    normal = (0, 0, -1)
    verts = [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5)]
    for tc, v in zip(tex, verts):
        vertex(normal, tc, v)

    # Esquerda
    normal = (-1, 0, 0)
    verts = [(-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5)]
    for tc, v in zip(tex, verts):
        vertex(normal, tc, v)

    # Direita
    normal = (1, 0, 0)
    verts = [(0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5)]
    for tc, v in zip(tex, verts):
        vertex(normal, tc, v)

    # Topo
    normal = (0, 1, 0)
    verts = [(-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)]
    for tc, v in zip(tex, verts):
        vertex(normal, tc, v)

    # Base
    normal = (0, -1, 0)
    verts = [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5)]
    for tc, v in zip(tex, verts):
        vertex(normal, tc, v)

    glEnd()

def desenhar_banco_modular(pos_x=0, textura_madeira=None, cam_pos=None):
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
            desenhar_retangulo_escalado(0, altura_assento, -0.12, comprimento_ripa, espessura, profundidade, cam_pos, True, textura_madeira)
            desenhar_retangulo_escalado(0, altura_assento,  0.12, comprimento_ripa, espessura, profundidade, cam_pos, True, textura_madeira)

            # Encosto
            glPushMatrix()
            glTranslatef(0, altura_encosto, -0.25)
            glRotatef(90, 1, 0, 0)
            desenhar_retangulo_escalado(0, 0, 0, comprimento_ripa, espessura, profundidade, cam_pos, True, textura_madeira)
            glPopMatrix()
        else:
            glColor3f(0.5, 0.3, 0.1)

        # Suportes
        glColor3f(0.1, 0.1, 0.1)
        for suporte_x in [-offset_perna, offset_perna]:
            desenhar_retangulo_escalado(suporte_x, altura_assento / 2, 0.12, 0.05, altura_assento, 0.05, cam_pos)
            desenhar_retangulo_escalado(suporte_x, altura_encosto / 2, -0.25, 0.05, altura_encosto, 0.05, cam_pos)

        glEndList()

    glPushMatrix()
    glTranslatef(pos_x, 0, 0)
    glCallList(banco_display_list)
    glPopMatrix()

def desenhar_bancos(lado, textura_madeira=None, distancia=4.28, cam_pos=None):
    glPushMatrix()
    glTranslatef(lado, 0, 0)

    def banco(x, z, rot):
        glPushMatrix()
        glTranslatef(x, 0, z)
        glRotatef(rot, 0, 1, 0)
        desenhar_banco_modular(0, textura_madeira, cam_pos)
        glPopMatrix()

    banco(0, distancia, 0)
    banco(-distancia, 0, -90)
    banco(0, -distancia, 180)
    banco(distancia, 0, 90)

    glPopMatrix()
