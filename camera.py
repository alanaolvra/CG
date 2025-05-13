# camera.py
import numpy as np
import math
import glfw

class Camera:
    def __init__(self):
        self.pos = np.array([0.0, 1.7, 15.0])
        self.front = np.array([0.0, 0.0, -1.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.yaw = -90.0
        self.pitch = 0.0
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True
        self.cursor_enabled = False  # estado atual do cursor

    def mouse_callback(self, window, xpos, ypos):
        if self.cursor_enabled:
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos
        self.last_x = xpos
        self.last_y = ypos

        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        self.pitch = max(min(self.pitch, 89.0), -89.0)

        front = [
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ]
        self.front = np.array(front) / np.linalg.norm(front)

    def process_input(self, window, delta_time):
        speed = 2.5 * delta_time
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.pos += speed * self.front
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.pos -= speed * self.front
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.pos -= np.cross(self.front, self.up) * speed
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.pos += np.cross(self.front, self.up) * speed
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            self.cursor_enabled = True
            self.first_mouse = True

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            if self.cursor_enabled:
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                self.cursor_enabled = False
                self.first_mouse = True 

def get_camera():
    return Camera()
