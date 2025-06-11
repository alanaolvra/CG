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
from desenhos.banco import desenhar_bancos
from desenhos.poste import desenhar_poste
from desenhos.grama import desenhar_grama
from desenhos.arvore import desenhar_arvore
from camera import get_camera
from colisao import get_colisao

colisao = get_colisao()
camera = get_camera()

def carregar_textura(path):
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
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1920 / 1080, 1, 100)
    glMatrixMode(GL_MODELVIEW)

    chao_textura = carregar_textura("images/chao.png")
    textura_madeira = carregar_textura("images/banco.jpeg")
    textura_grama = carregar_textura("images/grama.png")
    textura_folha = carregar_textura("images/folha.png")
    textura_tronco = carregar_textura("images/tronco.png")

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

        glfw.set_cursor_pos_callback(window, camera.mouse_callback)
        glfw.set_mouse_button_callback(window, camera.mouse_button_callback)
        
        desenhar_ceu()
        desenhar_chao(chao_textura)
        desenhar_relogio()
        desenhar_torre()
        desenhar_cristo()
        desenhar_grama(10, textura_grama)
        desenhar_grama(-10, textura_grama)
        desenhar_bancos(10, textura_madeira)
        desenhar_bancos(-10, textura_madeira)
        desenhar_poste(10)
        desenhar_poste(-10)
        desenhar_arvore(5, textura_folha, textura_tronco)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
