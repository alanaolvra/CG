# colisao.py
import numpy as np

class Colisao:
    def __init__(self):
        self.torre_pos = np.array([0.0, 0.0, 0.0])
        self.torre_size = np.array([1.0, 5.0, 1.0])  # largura, altura, profundidade
        self.chao_y = 1.7  # altura padrão da câmera, para não cair "abaixo do chão"

    def checar_colisao_chao(self, camera_pos):
        # Se a câmera estiver abaixo do chão, corrige a altura
        if camera_pos[1] < self.chao_y:
            camera_pos[1] = self.chao_y
        return camera_pos

    def checar_colisao_torre(self, camera_pos):
        # Checa colisão simples: se a câmera está dentro dos limites da torre
        torre_min = self.torre_pos - self.torre_size / 2
        torre_max = self.torre_pos + self.torre_size / 2

        buffer = 0.5  # margem de distância para a câmera não encostar direto na torre

        if (torre_min[0] - buffer <= camera_pos[0] <= torre_max[0] + buffer and
            torre_min[1] - buffer <= camera_pos[1] <= torre_max[1] + buffer and
            torre_min[2] - buffer <= camera_pos[2] <= torre_max[2] + buffer):
            
            # Afasta a câmera para fora da torre
            # Simples: empurra ela para trás na direção oposta à frente
            deslocamento = camera_pos - self.torre_pos
            deslocamento[1] = 0  # só considera X e Z para não "voar"
            deslocamento = deslocamento / np.linalg.norm(deslocamento) * (np.linalg.norm(self.torre_size)/2 + buffer)
            camera_pos[:2] = self.torre_pos[:2] + deslocamento[:2]
            
        return camera_pos

    def checar_colisoes(self, camera_pos):
        camera_pos = self.checar_colisao_chao(camera_pos)
        camera_pos = self.checar_colisao_torre(camera_pos)
        return camera_pos

def get_colisao():
    return Colisao()
