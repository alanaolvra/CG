import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame import image
from pygame.locals import *
import numpy as np
import math

# Câmera
camera_pos = np.array([0.0, 1.7, 8.0]) 
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw = -90.0
pitch = 0.0
last_x, last_y = 400, 300
first_mouse = True

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
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    return window

def mouse_callback(window, xpos, ypos):
    global last_x, last_y, first_mouse, yaw, pitch, camera_front
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos
    last_x = xpos
    last_y = ypos

    sensitivity = 0.1
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset
    pitch = max(min(pitch, 89.0), -89.0)

    front = [
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ]
    camera_front[:] = front / np.linalg.norm(front)

def process_input(window, delta_time):
    global camera_pos
    speed = 2.5 * delta_time

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        camera_pos += speed * camera_front
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        camera_pos -= speed * camera_front
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        camera_pos -= np.cross(camera_front, camera_up) * speed
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        camera_pos += np.cross(camera_front, camera_up) * speed
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
        

def desenhar_torre():
    glPushMatrix()
    glTranslatef(0, 2.5, 0)   # Eleva a torre acima do solo
    glScalef(1, 5, 1)         # Escala para fazer a torre vertical
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.2, 0.2)

    # Frente
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)

    # Trás
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)

    # Direita
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)

    # Esquerda
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5, -0.5)

    # Topo
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f( 0.5,  0.5, -0.5)

    # Base
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f(-0.5, -0.5,  0.5)

    glEnd()
    glPopMatrix()

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

def desenhar_chao(textura_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-20, 0, -20)
    glTexCoord2f(20, 0); glVertex3f(20, 0, -20)
    glTexCoord2f(20, 20); glVertex3f(20, 0, 20)
    glTexCoord2f(0, 20); glVertex3f(-20, 0, 20)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def main():
    pygame.init()
    window = init_window()
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)  # 45 graus de FOV, aspecto da janela, plano de corte próximo e distante
    glMatrixMode(GL_MODELVIEW)

    chao_textura = carregar_textura("piso_branco.jpeg")

    last_frame = glfw.get_time()
    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        process_input(window, delta_time)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        center = camera_pos + camera_front
        gluLookAt(*camera_pos, *center, *camera_up)

        desenhar_chao(chao_textura)
        desenhar_torre()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
