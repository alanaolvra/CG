from OpenGL.GL import *
from colisao import objetos_colisao
from colisao import calcular_bounding_box, transformar_bounding_box
from textura import carregar_textura, carregar_textura_PIL
import pywavefront

pessoa_modelo = None
pessoa_display_list = None
texturas_carregadas = {}


def carregar_pessoa():
    global pessoa_modelo, texturas_carregadas, pessoa_display_list

    try:
        # Carrega o modelo e materiais (com coleta de texturas ativada)
        pessoa_modelo = pywavefront.Wavefront(
            'script/cj4.obj',
            create_materials=True,
            collect_faces=True,
            parse=True
        )

        # Carrega as texturas
        for nome_material, material in pessoa_modelo.materials.items():
            if hasattr(material, 'texture') and material.texture is not None:
                textura_path = material.texture.path
                textura_id = carregar_textura_PIL(textura_path)
                if textura_id is not None:
                    texturas_carregadas[nome_material] = textura_id
        # Gera display list
        pessoa_display_list = glGenLists(1)
        glNewList(pessoa_display_list, GL_COMPILE)
        for mesh in pessoa_modelo.mesh_list:
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

        print("[✓] Modelo barraca carregado e cacheado com sucesso")

    except Exception as e:
        print(f"[Erro] Falha ao carregar modelo barraca: {e}")




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

    # Luz principal (direcional suave)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [4.0, 10.0, 10.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])

    # Luz de preenchimento (oposta à principal)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [-4.0, -2.0, -8.0, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.4, 0.4, 0.4, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])


def desenhar_pessoa(ladox, ladoz):
    global pessoa_modelo

    if pessoa_modelo is None:
        carregar_pessoa()
        bbox_pessoa = calcular_bounding_box(pessoa_modelo)
        bbox_pessoa = transformar_bounding_box(bbox_pessoa, [0.05, 0.05, 0.05], [5, 0, 12])
        objetos_colisao["Pessoa"] = bbox_pessoa

    glPushMatrix()

    configurar_iluminacao()
    glDisable(GL_CULL_FACE)

    glTranslatef(ladox, 1.5, ladoz)
    glRotatef(-90, 0, 1, 0)
    glScalef(0.95, 0.95, 0.95)

    if pessoa_display_list:
        glCallList(pessoa_display_list)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT1)
    glPopMatrix()

