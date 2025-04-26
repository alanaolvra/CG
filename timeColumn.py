import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame import image
from pygame.locals import *
from desenhos.chao import desenhar_chao
from desenhos.fundo import desenhar_ceu
from desenhos.relogio import desenhar_relogio
from desenhos.torre import desenhar_torre
from camera import get_camera
from colisao import get_colisao

colisao = get_colisao()
camera = get_camera()

def carregar_textura(path):
    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)
    img = image.load(path)
    img_data = pygame.image.tostring(img, "RGB", 1)
    width, height = img.get_rect().size
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return textura

def init_window():
    if not glfw.init():
        return None
    window = glfw.create_window(800, 600, "Coluna da Hora - Russas", None, None)
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    return window

def main():
    pygame.init()
    window = init_window()
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    chao_textura = carregar_textura("images/piso_branco.jpeg")

    last_frame = glfw.get_time()
    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        camera.process_input(window, delta_time)

        # Trata as colisões depois do movimento
        camera.pos = colisao.checar_colisoes(camera.pos)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        center = camera.pos + camera.front
        gluLookAt(*camera.pos, *center, *camera.up)

        desenhar_chao(chao_textura)
        desenhar_relogio()
        desenhar_ceu()
        desenhar_torre()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
