from OpenGL.GL import *
import pywavefront

barraca_modelo = None
def carregar_casa():
    global barraca_modelo, texturas_carregadas
    barraca_modelo = pywavefront.Wavefront(
        'script/barraca.obj',
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
    
    # --- LUZ 1: DE CIMA (POSICIONAL) ---
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    
    # Posição diretamente acima da barraca (x=8, z=14), y=5 é altura
    glLightfv(GL_LIGHT0, GL_POSITION, [8.0, 5.0, 14.0, 1.0])  # posicional

    # --- LUZ 2: DE FRENTE (DIRECIONAL) ---
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.01, 0.01, 0.01, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

    # Luz direcional vindo da frente da barraca em direção a ela
    # Se a barraca está em z=14, essa luz "vem de z=10 para z=14"
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 0.0, 1.0, 0.0])  # direcional

    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    

def desenhar_barraca(ladox, ladoz):
    if barraca_modelo is None:
        carregar_casa()

    glPushMatrix()
    configurar_iluminacao()
    
    # Transformação da casa
    glTranslatef(ladox, 0.2, ladoz)
    glRotatef(-90, 0, 1, 0)
    glScalef(0.3, 0.3, 0.3)

    # Renderização da casa
    for mesh in barraca_modelo.mesh_list:
            textura = None
            material = None
            if mesh.materials:
                material_name = mesh.materials[0].name
                material = barraca_modelo.materials.get(material_name)
                if material:
                    aplicar_material(material)

            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_index in face:
                    # Normais
                    if barraca_modelo.parser.normals:
                        try:
                            glNormal3f(*barraca_modelo.parser.normals[vertex_index])
                        except IndexError:
                            pass

                    # Vértices
                    glVertex3f(*barraca_modelo.vertices[vertex_index])
            glEnd()

    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT1)
    glPopMatrix()
