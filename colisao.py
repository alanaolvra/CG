import numpy as np

objetos_colisao = {}
class Colisao:
    def __init__(self):
        self.objetos = {}
        self.chao_y = 1.2

    def set_objetos(self, objetos):
        self.objetos = objetos
        
    def _verificar_colisao(self, pos, caixa, raio=0.3):
            px, pz = pos[0], pos[2]

            minx, maxx = caixa['min'][0], caixa['max'][0]
            minz, maxz = caixa['min'][2], caixa['max'][2]

            closest_x = max(minx, min(px, maxx))
            closest_z = max(minz, min(pz, maxz))

            dx = px - closest_x
            dz = pz - closest_z
            dist_squared = dx * dx + dz * dz

            return dist_squared < raio * raio

    def checar_colisoes(self, pos):
        pos = np.copy(pos)
        raio = 0.3
        pos[1] = max(pos[1], self.chao_y)

        for nome, caixa in self.objetos.items():
            if self._verificar_colisao(pos, caixa, raio):
                # Calcular distância do centro da caixa
                centro_x = (caixa['min'][0] + caixa['max'][0]) / 2
                centro_z = (caixa['min'][2] + caixa['max'][2]) / 2

                metade_x = (caixa['max'][0] - caixa['min'][0]) / 2
                metade_z = (caixa['max'][2] - caixa['min'][2]) / 2

                dist_x = pos[0] - centro_x
                dist_z = pos[2] - centro_z

                limite_x = metade_x + raio
                limite_z = metade_z + raio

                overlap_x = limite_x - abs(dist_x)
                overlap_z = limite_z - abs(dist_z)

                if overlap_x > 0 and overlap_z > 0:
                    if overlap_x < overlap_z:
                        pos[0] = centro_x + np.sign(dist_x) * limite_x
                    else:
                        pos[2] = centro_z + np.sign(dist_z) * limite_z

        return pos

def calcular_bounding_box(modelo):
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
