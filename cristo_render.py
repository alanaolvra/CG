from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

class Material:
    def __init__(self, name):
        self.name = name
        self.diffuse = (1.0, 1.0, 1.0)  # Cor difusa padrão branca
        self.specular = (1.0, 1.0, 1.0)  # Cor especular padrão branca
        self.ambient = (1.0, 1.0, 1.0)  # Cor ambiente padrão branca
        self.shininess = 0.0
        self.texture = None

    def set_material(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialf(GL_FRONT, GL_SHININESS, self.shininess)
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)

class OBJ:
    def __init__(self, filename, mtl_filename=None):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.materials = {}

        material = None

        if mtl_filename:
            self.load_materials(mtl_filename)

        with open(filename, "r") as f:
            for line in f:
                if line.startswith('#'): continue
                values = line.strip().split()
                if not values: continue

                if values[0] == 'v':
                    self.vertices.append(tuple(map(float, values[1:4])))
                elif values[0] == 'vn':
                    self.normals.append(tuple(map(float, values[1:4])))
                elif values[0] == 'vt':
                    self.texcoords.append(tuple(map(float, values[1:3])))
                elif values[0] == 'f':
                    face = []
                    for v in values[1:]:
                        w = v.split('/')
                        vertex_index = int(w[0]) - 1
                        tex_index = int(w[1]) - 1 if len(w) > 1 and w[1] else None
                        norm_index = int(w[2]) - 1 if len(w) > 2 and w[2] else None
                        face.append((vertex_index, tex_index, norm_index))
                    self.faces.append((face, material))
                elif values[0] == 'usemtl':
                    material = values[1]

        # Gera display list para performance
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)
        self._compile()
        glEndList()

    def load_materials(self, mtl_filename):
        current_material = None
        with open(mtl_filename, "r") as f:
            for line in f:
                values = line.strip().split()
                if not values: continue

                if values[0] == 'newmtl':
                    current_material = Material(values[1])
                    self.materials[current_material.name] = current_material
                elif values[0] == 'Kd':  # Diffuse color
                    current_material.diffuse = tuple(map(float, values[1:4]))
                elif values[0] == 'Ks':  # Specular color
                    current_material.specular = tuple(map(float, values[1:4]))
                elif values[0] == 'Ka':  # Ambient color
                    current_material.ambient = tuple(map(float, values[1:4]))
                elif values[0] == 'Ns':  # Shininess
                    current_material.shininess = float(values[1])

    def _compile(self):
        glBegin(GL_TRIANGLES)
        for face, material in self.faces:
            if material:
                mat = self.materials.get(material)
                if mat:
                    mat.set_material()

            for v in face:
                if v[2] is not None:
                    glNormal3fv(self.normals[v[2]])
                if v[1] is not None:
                    glTexCoord2fv(self.texcoords[v[1]])
                glVertex3fv(self.vertices[v[0]])
        glEnd()

    def render(self):
        glCallList(self.display_list)

def setup_lighting():
    # Ativar a luz
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Definir cor de luz ambiente
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))  # Luz ambiente suave

    # Definir cor da luz difusa
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  # Luz branca

    # Definir posição da luz (em coordenadas homogêneas)
    glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))  # Luz vindo de uma direção

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OBJ Viewer with Lighting - OpenGL")

    # Configurar fundo branco
    glClearColor(0.8, 0.8, 0.8, 1.0)  # Fundo cinza claro

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Configurar perspectiva
    gluPerspective(60, (800/600), 0.1, 1000.0)
    glTranslatef(0.0, -2.0, -15)  # Ajuste a posição da câmera
    glScalef(0.2, 0.2, 0.2)

    # Configuração da iluminação
    setup_lighting()

    obj = OBJ("script/cristo2.obj", "script/cristo2.mtl")
    print("Modelo carregado com", len(obj.vertices), "vértices e", len(obj.faces), "faces")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 0, 1, 0)  # Rotação simples
        obj.render()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
