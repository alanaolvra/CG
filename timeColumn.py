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
from desenhos.cristo import desenhar_cristo
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
    window = glfw.create_window(1920, 1080, "Coluna da Hora - Russas", None, None)
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    return window

def main():
    pygame.init()
    window = init_window()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_position = [0.0, 10.0, 10.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1920.0 / 1080.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    chao_textura = carregar_textura("images/piso_branco.jpeg")

    last_frame = glfw.get_time()
    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        camera.process_input(window, delta_time)

        camera.pos = colisao.checar_colisoes(camera.pos)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        center = camera.pos + camera.front
        gluLookAt(*camera.pos, *center, *camera.up)

        desenhar_chao(chao_textura)
        desenhar_relogio()
        desenhar_ceu()
        desenhar_torre()
        desenhar_cristo()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
