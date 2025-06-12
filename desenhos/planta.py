from OpenGL.GL import *
import pywavefront

planta_modelo = None
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
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1.0])

    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

def desenhar_planta(ladox, ladoz):
    if planta_modelo is None:
        carregar_planta()

    glPushMatrix()
    glTranslatef(ladox, 0, ladoz)
    glScalef(0.2, 0.2, 0.2)
    
    configurar_iluminacao()

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
                        pass
                glVertex3f(*planta_modelo.vertices[vertex_i][:3])
        glEnd()

    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_NORMALIZE)
        
    glPopMatrix()