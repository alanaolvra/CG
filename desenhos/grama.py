from OpenGL.GL import *
import numpy as np
from colisao import objetos_colisao, calcular_bounding_box, transformar_bounding_box


def phong_iluminacao(P, cam_pos, normal, mat_amb, mat_diff, mat_spec, mat_shine,
                     luz_pos=np.array([5.0, 10.0, 5.0]),
                     luz_amb=np.array([0.5, 0.5, 0.5]),
                     luz_diff=np.array([1.0, 1.0, 1.0]),
                     luz_spec=np.array([1.0, 1.0, 1.0]),
                     emissive=np.array([0.0, 0.0, 0.0])):

    # Reflexão ambiente
    ambient = luz_amb * mat_amb

    # Reflexão difusa
    L = luz_pos - P
    L = L / np.linalg.norm(L)
    N = normal / np.linalg.norm(normal)
    diff = luz_diff * mat_diff * max(np.dot(L, N), 0.0)

    # Reflexão especular
    V = cam_pos - P
    V = V / np.linalg.norm(V)
    R = 2 * np.dot(N, L) * N - L
    spec = luz_spec * mat_spec * (max(np.dot(V, R), 0.0) ** mat_shine)

    cor = ambient + diff + spec + emissive
    return np.clip(cor, 0.0, 1.0)


def desenhar_grama(lado, textura_grama, repeat=8):
    cam_pos = np.array([0.0, 5.0, 8.0])  # Ajuste conforme sua câmera real
    normal = np.array([0.0, 1.0, 0.0])   # Plano horizontal

    # Material da grama
    mat_amb = np.array([0.1, 0.4, 0.1])
    mat_diff = np.array([0.2, 0.8, 0.2])
    mat_spec = np.array([0.2, 0.5, 0.2])
    emissive = np.array([0.0, 0.0, 0.0])
    mat_shine = 16.0

    luz_pos = np.array([5.0, 10.0, 5.0])
    luz_amb = np.array([0.2, 0.2, 0.2])
    luz_diff = np.array([1.0, 1.0, 1.0])
    luz_spec = np.array([1.0, 1.0, 1.0])

    grama = 8
    y = 0.01

    bbox_grama = {
        "min": [-grama / 2, y, -grama / 2],
        "max": [ grama / 2, y,  grama / 2]
    }
    
    bbox_grama = transformar_bounding_box(bbox_grama, escala=[1.3,1.3,1.3], translacao=[lado,0,0])

    objetos_colisao[f"Grama_{lado}"] = bbox_grama

    vertices = [
        (-grama/2, y, -grama/2),
        ( grama/2, y, -grama/2),
        ( grama/2, y,  grama/2),
        (-grama/2, y,  grama/2)
    ]

    tex_coords = [
        (0, 0),
        (repeat, 0),
        (repeat, repeat),
        (0, repeat)
    ]

    glPushMatrix()
    glTranslatef(lado, 0, 0)
    glDisable(GL_LIGHTING)  # usando iluminação manual
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_grama)

    glBegin(GL_QUADS)
    for tex, v in zip(tex_coords, vertices):
        P = np.array(v)
        cor = phong_iluminacao(
            P, cam_pos, normal,
            mat_amb, mat_diff, mat_spec, mat_shine,
            luz_pos=luz_pos,
            luz_amb=luz_amb,
            luz_diff=luz_diff,
            luz_spec=luz_spec,
            emissive=emissive
        )

        glColor3fv(cor)
        glTexCoord2f(*tex)
        glNormal3fv(normal)
        glVertex3f(*v)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
