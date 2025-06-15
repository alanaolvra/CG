import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame import image
from pygame.locals import *

def carregar_textura(path):
    try:
        textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura)

        img = image.load(path)
        width, height = img.get_size()

        has_alpha = img.get_alpha() is not None
        mode = "RGBA" if has_alpha else "RGB"
        gl_format = GL_RGBA if has_alpha else GL_RGB

        img_data = pygame.image.tostring(img, mode, True)

        glTexImage2D(GL_TEXTURE_2D, 0, gl_format, width, height, 0, gl_format, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        return textura
    except Exception as e:
        print(f"Erro ao carregar a textura de {path}: {e}")
        return None