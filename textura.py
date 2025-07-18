from OpenGL.GL import *
from PIL import Image

def carregar_textura(path):
    try:
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        img = img.convert("RGBA")

        width, height = img.size
        img_data = img.tobytes()

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

        return textura

    except Exception as e:
        print(f"[Erro] Falha ao carregar textura com PIL '{path}': {e}")
        return None
