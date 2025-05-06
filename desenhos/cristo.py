from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

# Carregamento do modelo
cristo_modelo = None

def carregar_cristo():
    global cristo_modelo
    cristo_modelo = pywavefront.Wavefront(
        'script/cristo.obj',
        create_materials=True,
        collect_faces=True,
        parse=True
    )
    print("Materiais carregados:", cristo_modelo.materials)
    
def aplicar_material(material):
    if material is not None:
        # Definir as propriedades do material de ambiente, difuso e especular
        glMaterialfv(GL_FRONT, GL_AMBIENT, material.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, material.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, material.specular)
        glMaterialf(GL_FRONT, GL_SHININESS, material.shininess)
        glMaterialfv(GL_FRONT, GL_EMISSION, material.emission)
        glMaterialf(GL_FRONT, GL_DEPTH_SCALE, material.dissolve)

def configurar_iluminacao():
    # Definir a posição da luz (no espaço 3D)
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])  # Luz em (5, 5, 5)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # Luz branca difusa
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Luz branca especular
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def desenhar_cristo():
    global cristo_modelo

    if cristo_modelo is None:
        carregar_cristo()

    glPushMatrix()

    # Posicionar o Cristo no topo do relógio que está no topo da torre
    glTranslatef(0, 5, 0)   # Altura aproximada (torre + relógio)
    glScalef(0.09, 0.09, 0.09)   # Escala para não ficar grande demais

    # Ativar iluminação
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    for name, mesh in cristo_modelo.meshes.items():
        # Verificar se o material do mesh está disponível
        if name in cristo_modelo.materials:
            material = cristo_modelo.materials[name]
            aplicar_material(material)

        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*cristo_modelo.vertices[vertex_i])
        glEnd()

    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)

    glPopMatrix()
