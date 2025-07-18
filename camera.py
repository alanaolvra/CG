import numpy as np
import math
import glfw

from dialogo import estar_perto_da_pessoa, iniciar_dialogo, is_dialogo_ativo
import dialogo

class Camera:
    def __init__(self):
        self.pos = np.array([0.0, 1.2, 15.0], dtype=np.float32)
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.yaw = -90.0
        self.pitch = 0.0
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True
        self.cursor_enabled = False

    def enable_cursor(self, window):
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        self.cursor_enabled = True
        self.first_mouse = True

    def disable_cursor(self, window):
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        self.cursor_enabled = False
        self.first_mouse = True

    def mouse_callback(self, window, xpos, ypos):
        if self.cursor_enabled:
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = (xpos - self.last_x) * 0.1
        yoffset = (self.last_y - ypos) * 0.1
        self.last_x = xpos
        self.last_y = ypos

        self.yaw += xoffset
        self.pitch += yoffset
        self.pitch = max(min(self.pitch, 89.0), -89.0)

        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        front = np.array([
            math.cos(yaw_rad) * math.cos(pitch_rad),
            math.sin(pitch_rad),
            math.sin(yaw_rad) * math.cos(pitch_rad)
        ], dtype=np.float32)

        self.front[:] = front / np.linalg.norm(front)

    def process_input(self, window, delta_time):
        speed = 2.5 * delta_time
        right = np.cross(self.front, self.up)
        move_dir = np.array([self.front[0], 0, self.front[2]])
        move_dir = move_dir / np.linalg.norm(move_dir)

        nova_pos = self.pos.copy()

        if not is_dialogo_ativo():
            if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
                nova_pos += speed * move_dir
            if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
                nova_pos -= speed * move_dir
            if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
                nova_pos -= right * speed
            if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
                nova_pos += right * speed

        nova_pos[0] = max(-18.5, min(18.5, nova_pos[0]))
        nova_pos[2] = max(-18.5, min(18.5, nova_pos[2]))

        self.pos = nova_pos

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            self.enable_cursor(window)

        if glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
            if not self.f_key_pressed:
                self.f_key_pressed = True
                if is_dialogo_ativo():
                    dialogo.encerrar_dialogo()
                else:
                    if dialogo.estar_perto_da_pessoa(self.pos, self.front):
                        dialogo.iniciar_dialogo()
        else:
            self.f_key_pressed = False

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            if self.cursor_enabled:
                self.disable_cursor(window)            

def get_camera():
    return Camera()
