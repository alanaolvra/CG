# textura.py
import pygame
from pygame import image
from OpenGL.GL import *
from PIL import Image

def carregar_textura(path):
    try:
        # Carrega imagem
        img = image.load(path)
        # img = pygame.image.load(path)
        # img = pygame.transform.flip(img, False, True)  # <- Flip vertical
        width, height = img.get_size()

        # Determina formato
        has_alpha = img.get_alpha() is not None
        mode = "RGBA" if has_alpha else "RGB"
        gl_format = GL_RGBA if has_alpha else GL_RGB

        img_data = pygame.image.tostring(img, mode, True)

        # Gera e configura textura
        textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura)

        glTexImage2D(GL_TEXTURE_2D, 0, gl_format, width, height, 0, gl_format, GL_UNSIGNED_BYTE, img_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return textura

    except Exception as e:
        print(f"[Erro] Falha ao carregar textura '{path}': {e}")
        return None




def carregar_textura_PIL(path):
    try:
        # Carrega imagem com PIL
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        img = img.convert("RGBA")  # Força formato consistente

        width, height = img.size
        img_data = img.tobytes()

        # Gera e configura textura OpenGL
        textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura)

        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            width, height, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img_data
        )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #print(f"[✓] Textura carregada com PIL: {path}")
        return textura

    except Exception as e:
        print(f"[Erro] Falha ao carregar textura com PIL '{path}': {e}")
        return None
