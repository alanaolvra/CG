from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
from colisao import objetos_colisao
from colisao import calcular_bounding_box, transformar_bounding_box

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

def aplicar_material(material):
    if material is not None:
        if hasattr(material, 'ambient'):
            glMaterialfv(GL_FRONT, GL_AMBIENT, material.ambient)
        if hasattr(material, 'diffuse'):
            glMaterialfv(GL_FRONT, GL_DIFFUSE, material.diffuse)
        if hasattr(material, 'specular'):
            glMaterialfv(GL_FRONT, GL_SPECULAR, material.specular)
        if hasattr(material, 'emissive'):
            glMaterialfv(GL_FRONT, GL_EMISSION, material.emissive)
        if hasattr(material, 'shininess'):
            glMaterialf(GL_FRONT, GL_SHININESS, min(material.shininess, 128.0))

def configurar_iluminacao():
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

def desenhar_cristo():
    global cristo_modelo, cristo_display_list

    if cristo_modelo is None:
        carregar_cristo()
        bbox_cristo = calcular_bounding_box(cristo_modelo)
        bbox_cristo = transformar_bounding_box(bbox_cristo, [0.08, 0.08, 0.08], [0, 5.06, 0])
        objetos_colisao["Cristo"] = bbox_cristo

    if cristo_display_list is None:
        cristo_display_list = glGenLists(1)
        glNewList(cristo_display_list, GL_COMPILE)

        glPushMatrix()
        glShadeModel(GL_SMOOTH)
        glTranslatef(0, 5.06, 0)
        glScalef(0.08, 0.08, 0.08)

        for mesh in cristo_modelo.mesh_list:
            material = None
            if mesh.materials:
                material_name = mesh.materials[0].name
                material = cristo_modelo.materials.get(material_name)

            if material:
                aplicar_material(material)
            else:
                glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
                glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
                glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
                glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    if cristo_modelo.parser.normals:
                        try:
                            glNormal3f(*cristo_modelo.parser.normals[vertex_i])
                        except IndexError:
                            glNormal3f(0.0, 1.0, 0.0)  # normal default
                    glVertex3f(*cristo_modelo.vertices[vertex_i])
            glEnd()

        glPopMatrix()
        glEndList()

    # Renderização real
    glPushMatrix()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    glCallList(cristo_display_list)

    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_NORMALIZE)
    glPopMatrix()
