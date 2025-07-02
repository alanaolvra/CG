from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pywavefront

cristo_modelo = None
cristo_display_list = None

def carregar_cristo():
    global cristo_modelo
    cristo_modelo = pywavefront.Wavefront(
        'script/cristo.obj',
        create_materials=True,
        collect_faces=True,
        parse=True,
        strict=False
    )

def phong_iluminacao(P, cam_pos, normal, mat_amb, mat_diff, mat_spec, mat_shine,
                     luz_pos=np.array([5.0, 10.0, 10.0]),
                     luz_amb=np.array([0.5, 0.5, 0.5]),
                     luz_diff=np.array([1.0, 1.0, 1.0]),
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

def desenhar_cristo():
    global cristo_modelo, cristo_display_list

    if cristo_modelo is None:
        carregar_cristo()

    if cristo_display_list is None:
        cristo_display_list = glGenLists(1)
        glNewList(cristo_display_list, GL_COMPILE)

        glPushMatrix()
        glShadeModel(GL_SMOOTH)
        glTranslatef(0, 5.06, 0)
        glScalef(0.08, 0.08, 0.08)

        for mesh in cristo_modelo.mesh_list:
            # Material base (ou valores fixos)
            mat_amb=np.array([1.0, 1.0, 1.0])
            mat_diff=np.array([1.0, 1.0, 1.0])
            mat_spec=np.array([1.0, 1.0, 1.0])
            mat_shine=128.0

            if mesh.materials:
                material_name = mesh.materials[0].name
                material = cristo_modelo.materials.get(material_name)
                if material:
                    if hasattr(material, 'ambient'):
                        mat_amb = np.array(material.ambient[:3])
                    if hasattr(material, 'diffuse'):
                        mat_diff = np.array(material.diffuse[:3])
                    if hasattr(material, 'specular'):
                        mat_spec = np.array(material.specular[:3])
                    if hasattr(material, 'shininess'):
                        mat_shine = float(material.shininess)

            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    P = np.array(cristo_modelo.vertices[vertex_i])
                    try:
                        normal = np.array(cristo_modelo.parser.normals[vertex_i])
                    except (IndexError, AttributeError):
                        normal = np.array([0.0, 1.0, 0.0])

                    cor = phong_iluminacao(
                        P,
                        cam_pos=np.array([0.0, 0.0, 20.0]),
                        normal=normal,
                        mat_amb=mat_amb,
                        mat_diff=mat_diff,
                        mat_spec=mat_spec,
                        mat_shine=mat_shine
                    )


                    glColor3f(*cor)
                    glNormal3f(*normal)
                    glVertex3f(*P)
            glEnd()

        glPopMatrix()
        glEndList()

    # Renderização
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)

    glCallList(cristo_display_list)

    glDisable(GL_NORMALIZE)
    glPopMatrix()
