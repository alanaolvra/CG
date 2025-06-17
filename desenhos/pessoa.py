# from OpenGL.GL import *
# import pywavefront
# from colisao import objetos_colisao
# from colisao import calcular_bounding_box, transformar_bounding_box
# from textura import carregar_textura

# pessoa_modelo = None
# texturas_carregadas = {}

# def carregar_pessoa():
#     global pessoa_modelo, texturas_carregadas
#     pessoa_modelo = pywavefront.Wavefront(
#         'script/humano4.obj',
#         create_materials=True,
#         collect_faces=True,
#         parse=True,
#         strict=False
#     )

#     print("Modelo carregado:", pessoa_modelo is not None)
#     print("Meshes carregadas:", len(pessoa_modelo.mesh_list))

#     for name, material in pessoa_modelo.materials.items():
#         texture_path = getattr(material, 'texture', None)
#         if texture_path and hasattr(texture_path, 'image_name'):
#             path = texture_path.image_name
#             textura = carregar_textura(path)
#             texturas_carregadas[name] = textura

# def aplicar_material(material, nome_textura=None):
#     if material is not None:
#         if hasattr(material, 'ambient'):
#             glMaterialfv(GL_FRONT, GL_AMBIENT, material.ambient)
#         if hasattr(material, 'diffuse'):
#             glMaterialfv(GL_FRONT, GL_DIFFUSE, material.diffuse)
#         if hasattr(material, 'specular'):
#             glMaterialfv(GL_FRONT, GL_SPECULAR, material.specular)
#         if hasattr(material, 'emissive'):
#             glMaterialfv(GL_FRONT, GL_EMISSION, material.emissive)
#         if hasattr(material, 'shininess'):
#             glMaterialf(GL_FRONT, GL_SHININESS, min(material.shininess, 128.0))

#     if nome_textura and nome_textura in texturas_carregadas:
#         glEnable(GL_TEXTURE_2D)
#         glBindTexture(GL_TEXTURE_2D, texturas_carregadas[nome_textura])
#     else:
#         glDisable(GL_TEXTURE_2D)

# def configurar_iluminacao():
#     glEnable(GL_LIGHTING)
#     glShadeModel(GL_SMOOTH)
#     glEnable(GL_NORMALIZE)

#     # Luz principal (direcional suave)
#     glEnable(GL_LIGHT0)
#     glLightfv(GL_LIGHT0, GL_POSITION, [4.0, 10.0, 10.0, 1.0])
#     glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
#     glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
#     glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])

#     # Luz de preenchimento (oposta à principal)
#     glEnable(GL_LIGHT1)
#     glLightfv(GL_LIGHT1, GL_POSITION, [-4.0, -2.0, -8.0, 1.0])
#     glLightfv(GL_LIGHT1, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
#     glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.4, 0.4, 0.4, 1.0])
#     glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])


# def desenhar_pessoa(ladox, ladoz):
#     global pessoa_modelo

#     if pessoa_modelo is None:
#         carregar_pessoa()
#         bbox_pessoa = calcular_bounding_box(pessoa_modelo)
#         bbox_pessoa = transformar_bounding_box(bbox_pessoa, [0.05, 0.05, 0.05], [9, 0, 10])
#         objetos_colisao["Pessoa"] = bbox_pessoa

#     glPushMatrix()

#     configurar_iluminacao()
#     glDisable(GL_CULL_FACE)

#     glTranslatef(ladox, 0, ladoz)
#     glRotatef(-90, 0, 1, 0)
#     glScalef(1, 1, 1)

#     for mesh in pessoa_modelo.mesh_list:
#         material = None
#         material_name = None

#         if mesh.materials:
#             material_name = mesh.materials[0].name
#             material = pessoa_modelo.materials.get(material_name)

#         aplicar_material(material, material_name)
#         glEnable(GL_TEXTURE_2D)
#         glBindTexture(GL_TEXTURE_2D, texturas_carregadas[material.name])

#         glBegin(GL_TRIANGLES)
#         for face in mesh.faces:
#             for vertex_index in face:
#                 # Coordenadas UV
#                 if pessoa_modelo.parser.tex_coords:
#                     try:
#                         glTexCoord2f(*pessoa_modelo.parser.tex_coords[vertex_index])
#                     except IndexError:
#                         pass
#                 # Normais
#                 if pessoa_modelo.parser.normals:
#                     try:
#                         glNormal3f(*pessoa_modelo.parser.normals[vertex_index])
#                     except IndexError:
#                         pass
#                 # Vértices
#                 glVertex3f(*pessoa_modelo.vertices[vertex_index])
#         glEnd()


#     glDisable(GL_TEXTURE_2D)
#     glDisable(GL_LIGHTING)
#     glDisable(GL_LIGHT1)
#     glPopMatrix()
