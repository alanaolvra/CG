from OpenGL.GL import *
import pywavefront
from colisao import objetos_colisao
from colisao import calcular_bounding_box, transformar_bounding_box

planta_modelo = None
planta_display_list = None

def carregar_planta():
    global planta_modelo
    planta_modelo = pywavefront.Wavefront(
        'script/planta.obj',
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
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    glLightfv(GL_LIGHT0, GL_POSITION, [3.0, 6.0, 3.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1.0])

    glShadeModel(GL_SMOOTH)

def desenhar_planta(ladox, ladoz):
    global planta_modelo, planta_display_list

    if planta_modelo is None:
        carregar_planta()
        planta_posicoes = [[3, 0, 5], [3, 0, -5], [-3, 0, -5], [-3, 0, 5]]
        for i, pos in enumerate(planta_posicoes):
            bbox = calcular_bounding_box(planta_modelo)
            bbox = transformar_bounding_box(bbox, [0.2, 0.2, 0.2], pos)
            objetos_colisao[f"Planta{i}"] = bbox

    if planta_display_list is None:
        planta_display_list = glGenLists(1)
        glNewList(planta_display_list, GL_COMPILE)

        glPushMatrix()
        glScalef(0.2, 0.2, 0.2)

        for mesh in planta_modelo.mesh_list:
            material = None
            if mesh.materials:
                material_name = mesh.materials[0].name
                material = planta_modelo.materials.get(material_name)

            if material:
                aplicar_material(material)
            else:
                glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.1, 0.05, 1.0]) 
                glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.4, 0.2, 0.1, 1.0])  
                glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1.0])
                glMaterialf(GL_FRONT, GL_SHININESS, 20.0)

            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    if planta_modelo.parser.normals:
                        try:
                            glNormal3f(*planta_modelo.parser.normals[vertex_i])
                        except IndexError:
                            glNormal3f(0.0, 1.0, 0.0)  # fallback
                    glVertex3f(*planta_modelo.vertices[vertex_i][:3])
            glEnd()

        glPopMatrix()
        glEndList()

    glPushMatrix()
    glTranslatef(ladox, 0, ladoz)
    configurar_iluminacao()
    glCallList(planta_display_list)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_NORMALIZE)
    glPopMatrix()
