from OpenGL.GL import *
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

def aplicar_material(material):
    if material:
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
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 10.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])
    glShadeModel(GL_SMOOTH)

def desenhar_poste(lado):
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
            material = None
            if mesh.materials:
                material_name = mesh.materials[0].name
                material = poste_modelo.materials.get(material_name)

            if material:
                aplicar_material(material)
            else:
                # fallback material
                glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
                glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
                glMaterialfv(GL_FRONT, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])
                glMaterialf(GL_FRONT, GL_SHININESS, 30.0)

            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    if poste_modelo.parser.normals:
                        try:
                            glNormal3f(*poste_modelo.parser.normals[vertex_i])
                        except IndexError:
                            glNormal3f(0.0, 1.0, 0.0)  # fallback normal
                    glVertex3f(*poste_modelo.vertices[vertex_i])
            glEnd()

        glPopMatrix()
        glEndList()

    glPushMatrix()
    glTranslatef(lado, 0, 0)
    configurar_iluminacao()
    glCallList(poste_display_list)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_NORMALIZE)
    glPopMatrix()
