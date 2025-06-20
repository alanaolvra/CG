import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from desenhos.pessoa import desenhar_pessoa
from desenhos.chao import desenhar_chao
from desenhos.fundo import desenhar_ceu
from desenhos.pessoa import desenhar_pessoa
from desenhos.relogio import desenhar_relogio
from desenhos.torre import desenhar_torre
from desenhos.cristo import desenhar_cristo
from desenhos.banco import desenhar_bancos
from desenhos.poste import desenhar_poste
from desenhos.grama import desenhar_grama
from desenhos.artesanato import desenhar_artesanato
from desenhos.cafe import desenhar_cafe
from desenhos.palmeira import desenhar_palmeira
from desenhos.burguer import desenhar_burguer
from camera import get_camera
from colisao import get_colisao
import dialogo
from textura import carregar_textura
from colisao import objetos_colisao

colisao = get_colisao()
camera = get_camera()

def init_window():
    if not glfw.init():
        return None
    window = glfw.create_window(1920, 1080, "Coluna da Hora - Russas", None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glfw.set_cursor_pos_callback(window, camera.mouse_callback)
    glfw.set_mouse_button_callback(window, camera.mouse_button_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # Adiciona os novos callbacks de teclado
    glfw.set_key_callback(window, dialogo.tratar_evento_tecla)
    glfw.set_char_callback(window, dialogo.tratar_evento_char)

    return window



def main():
    pygame.init()
    window = init_window()
    if window is None:
        print("Erro ao inicializar janela.")
        return

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1920 / 1080, 1, 100)
    glMatrixMode(GL_MODELVIEW)

    # Carrega texturas uma vez
    chao_textura = carregar_textura("images/chao.png")
    textura_madeira = carregar_textura("images/banco.jpeg")
    textura_grama = carregar_textura("images/grama.png")

    last_frame = glfw.get_time()

    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        camera.process_input(window, delta_time)
        
        colisao.set_objetos(objetos_colisao)
        camera.pos = colisao.checar_colisoes(camera.pos)
        


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        center = camera.pos + camera.front
        gluLookAt(*camera.pos, *center, *camera.up)

        # Renderiza cena
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
        desenhar_palmeira(7, 0)
        desenhar_palmeira(13, 0)
        desenhar_palmeira(-7, 0)
        desenhar_palmeira(-13, 0)
        desenhar_burguer(10, 10.5)
        desenhar_pessoa(5.6, 10.2)
        desenhar_artesanato(-10, -10)
        desenhar_cafe(-10, 12)
        

        if dialogo.is_dialogo_ativo():
            dialogo.desenhar_overlay(delta_time)

        glfw.swap_buffers(window)   
        glfw.poll_events()


    glfw.terminate()



if __name__ == "__main__":
    main()