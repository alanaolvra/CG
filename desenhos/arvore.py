from OpenGL.GL import *
import pywavefront

arvore_modelo = None
def carregar_arvore():
    global arvore_modelo
    arvore_modelo = pywavefront.Wavefront(
        'script/arvore.obj',
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
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 10.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])

    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

def desenhar_arvore(lado, textura_folha, textura_tronco):
    if arvore_modelo is None:
        carregar_arvore()

    glPushMatrix()
    glTranslatef(lado, 0, 0)
    glScalef(0.2, 0.2, 0.2)
    glRotatef(90, 0, 1, 0)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.1)
    
    configurar_iluminacao()

    for mesh in arvore_modelo.mesh_list:
        mat = arvore_modelo.materials.get(mesh.materials[0])
        aplicar_material(mat)
        
        # Seleção de textura
        tex_path = getattr(getattr(mat, 'texture', None), 'path', '').lower()
        if 'Palm_4_Leaf' in tex_path:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, textura_folha)
        elif 'Plam_4_Trunk' in tex_path:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, textura_tronco)
        else:
            glDisable(GL_TEXTURE_2D)

        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                if vertex_i < len(arvore_modelo.parser.normals):
                    glNormal3f(*arvore_modelo.parser.normals[vertex_i])
                
                if vertex_i < len(arvore_modelo.parser.tex_coords):
                    glTexCoord2f(*arvore_modelo.parser.tex_coords[vertex_i])
                
                glVertex3f(*arvore_modelo.vertices[vertex_i])
        glEnd()
        
        glDisable(GL_TEXTURE_2D)

    glDisable(GL_BLEND)
    glDisable(GL_ALPHA_TEST)
    glDisable(GL_LIGHTING)
    glPopMatrix()