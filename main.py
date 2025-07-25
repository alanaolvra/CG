import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import pygame
from pygame.locals import *
from desenhos.ceramica import desenhar_ceramica
from desenhos.frutas import desenhar_frutas
from desenhos.pessoa import desenhar_pessoa
from desenhos.chao import desenhar_chao
from desenhos.fundo import desenhar_ceu
from desenhos.pessoa import desenhar_pessoa
from desenhos.relogio import desenhar_relogio
from desenhos.tapetes import desenhar_tapete
from desenhos.torre import desenhar_torre
from desenhos.cristo import desenhar_cristo
from desenhos.banco import desenhar_bancos
from desenhos.poste import desenhar_poste
from desenhos.grama import desenhar_grama
from desenhos.restaurante import desenhar_restaurante
from desenhos.palmeira import desenhar_palmeira
from desenhos.burguer import desenhar_burguer
from desenhos.grade import desenhar_grade
from desenhos.agua import desenhar_agua
from desenhos.fundo import desenhar_ceu
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
    
    glfw.window_hint(glfw.SAMPLES, 8)

    window = glfw.create_window(1920, 1080, "Coluna da Hora - Russas", None, None)
    icon = "images/icon.jpg"
    glfw.set_window_icon(window, 1, Image.open(icon))
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
    glEnable(GL_MULTISAMPLE)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1920 / 1080, 1, 100)
    glMatrixMode(GL_MODELVIEW)

    # Carrega texturas uma vez
    chao_textura = carregar_textura("images/chao.png")
    textura_madeira = carregar_textura("images/banco.jpeg")
    textura_grama = carregar_textura("images/grama.png")
    textura_agua = carregar_textura("images/agua.png")
    textura_rua = carregar_textura("images/rua.jpg")
    textura_ceu = carregar_textura("images/ceu.png")
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
        desenhar_ceu(textura_rua, textura_ceu)
        desenhar_chao(chao_textura)
        desenhar_relogio()
        desenhar_torre()
        desenhar_cristo(cam_pos=camera.pos)
        desenhar_bancos(10, textura_madeira, cam_pos=camera.pos)
        desenhar_bancos(-10, textura_madeira, cam_pos=camera.pos)
        desenhar_grama(10, textura_grama, cam_pos=camera.pos)
        desenhar_grama(-10, textura_grama, cam_pos=camera.pos)
        desenhar_poste(10, cam_pos=camera.pos)
        desenhar_poste(-10, cam_pos=camera.pos)
        desenhar_palmeira(7, 0)
        desenhar_palmeira(13, 0)
        desenhar_palmeira(-7, 0)
        desenhar_palmeira(-13, 0)
        desenhar_restaurante(-10, 12)
        desenhar_burguer(10, 12.5)
        desenhar_pessoa(5, 12)
        desenhar_tapete(-8, -10)
        desenhar_ceramica(-3, -10)
        desenhar_frutas(4, -10)
        desenhar_agua(textura_agua)
        desenhar_grade()

        if dialogo.is_dialogo_ativo():
            dialogo.desenhar_overlay(delta_time)

        glfw.swap_buffers(window)   
        glfw.poll_events()


    glfw.terminate()

if __name__ == "__main__":
    main()