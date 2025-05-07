from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

cristo_modelo = None
def carregar_cristo():
    global cristo_modelo
    cristo_modelo = pywavefront.Wavefront(
        'script/cristo.obj',
        create_materials=True,
        collect_faces=True,
        parse=True,
        strict=False
    )
    print("Normais carregadas:", len(cristo_modelo.parser.normals))
    print("Materiais carregados:", cristo_modelo.materials)
    print("Número total de vértices:", len(cristo_modelo.vertices))
    total_faces = sum(len(mesh.faces) for mesh in cristo_modelo.mesh_list)
    print("Número total de faces (triângulos):", total_faces)
    print("Nomes das malhas:", [mesh.name for mesh in cristo_modelo.mesh_list])
    print("Número de malhas:", len(cristo_modelo.mesh_list))
    
    
def aplicar_material(material):
    if material is not None:
        #getattr() para evitar erros se atributos estiverem faltando
        glMaterialfv(GL_FRONT, GL_AMBIENT, getattr(material, 'ambient', [0.2, 0.2, 0.2, 1.0]))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, getattr(material, 'diffuse', [0.8, 0.8, 0.8, 1.0]))
        glMaterialfv(GL_FRONT, GL_SPECULAR, getattr(material, 'specular', [0.0, 0.0, 0.0, 1.0]))
        glMaterialfv(GL_FRONT, GL_EMISSION, getattr(material, 'emissive', [0.0, 0.0, 0.0, 1.0]))
        shininess = min(getattr(material, 'shininess', 0.0), 128.0)
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)

def configurar_iluminacao():
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def desenhar_cristo():
    global cristo_modelo

    if cristo_modelo is None:
        carregar_cristo()

    glPushMatrix()
    glTranslatef(0, 5.05, 0)
    glScalef(0.09, 0.09, 0.09)
    glEnable(GL_NORMALIZE)

    configurar_iluminacao()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    for mesh in cristo_modelo.mesh_list:
        if mesh.materials:
            material_name = mesh.materials[0].name
            material = cristo_modelo.materials.get(material_name)
            if material:
                aplicar_material(material)
        
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                if cristo_modelo.parser.normals:
                    try:
                        glNormal3f(*cristo_modelo.parser.normals[vertex_i])
                    except IndexError:
                        pass
                glVertex3f(*cristo_modelo.vertices[vertex_i])
        glEnd()
        
    glDisable(GL_LIGHTING)
    glPopMatrix()
