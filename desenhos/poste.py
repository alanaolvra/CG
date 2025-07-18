from OpenGL.GL import *
import numpy as np
import pywavefront

poste_modelo = None
poste_display_list = None

def carregar_poste():
    global poste_modelo
    poste_modelo = pywavefront.Wavefront(
        'script/poste.obj',
        create_materials=True,
        collect_faces=True,
        parse=True,
        strict=False
    )

def phong_iluminacao(P, cam_pos, normal, mat_amb, mat_diff, mat_spec, mat_shine,
                     luz_pos=np.array([5.0, 10.0, 5.0]),
                     luz_amb=np.array([0.5, 0.5, 0.5]),
                     luz_diff=np.array([1.0, 1.0, 1.0]),
                     luz_spec=np.array([1.0, 1.0, 1.0]),
                     emissive=np.array([0.0, 0.0, 0.0])):

    ambient = luz_amb * mat_amb
    L = luz_pos - P
    L = L / np.linalg.norm(L)
    N = normal / np.linalg.norm(normal)
    diff = luz_diff * mat_diff * max(np.dot(L, N), 0.0)

    V = cam_pos - P
    V = V / np.linalg.norm(V)
    R = 2 * np.dot(N, L) * N - L
    spec = luz_spec * mat_spec * (max(np.dot(V, R), 0.0) ** mat_shine)

    cor = ambient + diff + spec + emissive
    return np.clip(cor, 0.0, 1.0)

def desenhar_poste(lado, cam_pos):
    global poste_modelo, poste_display_list

    if poste_modelo is None:
        carregar_poste()

    if poste_display_list is None:
        poste_display_list = glGenLists(1)
        glNewList(poste_display_list, GL_COMPILE)

        glPushMatrix()
        glScalef(0.2, 0.2, 0.2)
        glRotatef(90, 0, 1, 0)

        for mesh in poste_modelo.mesh_list:
            mat_amb = np.array([0.2, 0.2, 0.2])
            mat_diff = np.array([0.5, 0.5, 0.5])
            mat_spec = np.array([0.5, 0.5, 0.5])
            emissive = np.array([0.0, 0.0, 0.0])
            mat_shine = 32.0

            if mesh.materials:
                material_name = mesh.materials[0].name
                material = poste_modelo.materials.get(material_name)
                if material:
                    if hasattr(material, 'ambient'):
                        mat_amb = np.array(material.ambient[:3])
                    if hasattr(material, 'diffuse'):
                        mat_diff = np.array(material.diffuse[:3])
                    if hasattr(material, 'specular'):
                        mat_spec = np.array(material.specular[:3])
                    if hasattr(material, 'shininess'):
                        mat_shine = float(material.shininess)
                    if hasattr(material, 'emissive'):
                        emissive = np.array(material.emissive[:3])

            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    P = np.array(poste_modelo.vertices[vertex_i])
                    try:
                        normal = np.array(poste_modelo.parser.normals[vertex_i])
                    except (IndexError, AttributeError):
                        normal = np.array([0.0, 1.0, 0.0])

                    cor = phong_iluminacao(
                        P,
                        cam_pos=cam_pos,
                        normal=normal,
                        mat_amb=mat_amb,
                        mat_diff=mat_diff,
                        mat_spec=mat_spec,
                        mat_shine=mat_shine,
                        emissive=emissive
                    )

                    glColor3f(*cor)
                    glNormal3f(*normal)
                    glVertex3f(*P)
            glEnd()

        glPopMatrix()
        glEndList()

    glPushMatrix()
    glTranslatef(lado, 0, 0)
    glDisable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glCallList(poste_display_list)
    glDisable(GL_NORMALIZE)
    glPopMatrix()
