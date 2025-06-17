# colisao.py
import numpy as np

objetos_colisao = {}
class Colisao:
    def __init__(self):
        self.objetos = {}
        self.chao_y = 1.7

    def set_objetos(self, objetos):
        """
        Define as caixas de colisão do cenário.
        objetos: dict {nome: {"min": [x,y,z], "max": [x,y,z]}}
        """
        self.objetos = objetos

    def checar_colisoes(self, pos):
        pos = np.copy(pos)
        raio = 0.3
        pos[1] = max(pos[1], self.chao_y)

        for nome, caixa in self.objetos.items():
            if self._verificar_colisao(pos, caixa, raio):
                # Corrige separadamente os eixos X e Z para permitir "deslizar"
                for i in [0, 2]:  # eixo X (0) e Z (2)
                    centro = (caixa['min'][i] + caixa['max'][i]) / 2
                    metade = (caixa['max'][i] - caixa['min'][i]) / 2
                    distancia = pos[i] - centro
                    limite = metade + raio

                    if abs(distancia) < limite:
                        # Trava o movimento no eixo se ultrapassou o limite
                        pos[i] = centro + np.sign(distancia) * limite

        return pos



    def _verificar_colisao(self, pos, caixa, raio=0.3):
        """
        Verifica colisão entre uma esfera 2D (XZ) com raio e uma AABB.
        """
        # Posição da câmera
        px, pz = pos[0], pos[2]

        # Caixa do objeto
        minx, maxx = caixa['min'][0], caixa['max'][0]
        minz, maxz = caixa['min'][2], caixa['max'][2]

        # Encontra o ponto mais próximo da caixa à posição (clamping)
        closest_x = max(minx, min(px, maxx))
        closest_z = max(minz, min(pz, maxz))

        # Calcula distância entre ponto e a caixa
        dx = px - closest_x
        dz = pz - closest_z
        dist_squared = dx * dx + dz * dz

        return dist_squared < raio * raio


# Funções utilitárias fora da classe

def calcular_bounding_box(modelo):
    """
    Retorna a bounding box (AABB) de um modelo carregado com pywavefront.
    """
    if not modelo or not modelo.vertices:
        return None

    xs = [v[0] for v in modelo.vertices]
    ys = [v[1] for v in modelo.vertices]
    zs = [v[2] for v in modelo.vertices]

    return {
        "min": [min(xs), min(ys), min(zs)],
        "max": [max(xs), max(ys), max(zs)],
    }

def transformar_bounding_box(caixa, escala, translacao):
    """
    Aplica escala e translação a uma bounding box.
    escala: [sx, sy, sz]
    translacao: [tx, ty, tz]
    """
    if not caixa:
        return None

    min_tr = [
        caixa['min'][i] * escala[i] + translacao[i] for i in range(3)
    ]
    max_tr = [
        caixa['max'][i] * escala[i] + translacao[i] for i in range(3)
    ]
    return {"min": min_tr, "max": max_tr}

def get_colisao():
    return Colisao()
