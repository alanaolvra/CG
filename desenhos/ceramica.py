from OpenGL.GL import *
import pywavefront
from colisao import objetos_colisao
from colisao import calcular_bounding_box, transformar_bounding_box
from textura import carregar_textura, carregar_textura_PIL

ceramica_modelo = None
ceramica_display_list = None
texturas_carregadas = {}

def carregar_ceramica():
    global ceramica_modelo, texturas_carregadas, ceramica_display_list
    try:
        ceramica_modelo = pywavefront.Wavefront(
            'script/ceramica.obj',
            create_materials=True,
            collect_faces=True,
            parse=True
        )

        # Carrega texturas
        for nome_material, material in ceramica_modelo.materials.items():
            if hasattr(material, 'texture') and material.texture is not None:
                textura_path = material.texture.path
                textura_id = carregar_textura_PIL(textura_path)
                if textura_id is not None:
                    texturas_carregadas[nome_material] = textura_id

        # Gera display list
        ceramica_display_list = glGenLists(1)
        glNewList(ceramica_display_list, GL_COMPILE)
        for mesh in ceramica_modelo.mesh_list:
            for material in mesh.materials:
                aplicar_material(material, material.name)
                if material.name in texturas_carregadas:
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, texturas_carregadas[material.name])
                else:
                    glDisable(GL_TEXTURE_2D)

                glBegin(GL_TRIANGLES)
                vertices = material.vertices
                for i in range(0, len(vertices), 8):
                    u, v     = vertices[i], vertices[i+1]
                    nx, ny, nz = vertices[i+2:i+5]
                    x, y, z  = vertices[i+5:i+8]
                    glTexCoord2f(u, v)
                    glNormal3f(nx, ny, nz)
                    glVertex3f(x, y, z)
                glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

        #print("[✓] Modelo ceramica carregado e cacheado com sucesso")

    except Exception as e:
        print(f"[Erro] Falha ao carregar modelo ceramica: {e}")




def aplicar_material(material, nome_textura=None):
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

    if nome_textura and nome_textura in texturas_carregadas:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texturas_carregadas[nome_textura])
    else:
        glDisable(GL_TEXTURE_2D)

            
def configurar_iluminacao():
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    
    #LUZ 1: DE CIMA (POSICIONAL)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [8.0, 5.0, 14.0, 1.0])

    #LUZ 2: De trás (DIRECIONAL)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.01, 0.01, 0.01, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT1, GL_POSITION, [-1.0, 0.0, -1.0, 0.0])

    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

def desenhar_ceramica(ladox, ladoz):
    global ceramica_modelo, ceramica_display_list

    if ceramica_modelo is None:
        carregar_ceramica()
        bbox_ceramica = calcular_bounding_box(ceramica_modelo)
        bbox_ceramica = transformar_bounding_box(bbox_ceramica, [1.7, 1, 3.7], [-3, 0, -10])
        objetos_colisao["ceramica"] = bbox_ceramica

    glPushMatrix()
    configurar_iluminacao()
    glDisable(GL_CULL_FACE)

    glTranslatef(ladox, 0, ladoz)
    glScalef(1.2, 1.2, 1.2)

    if ceramica_display_list:
        glCallList(ceramica_display_list)

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT1)
    glPopMatrix()
