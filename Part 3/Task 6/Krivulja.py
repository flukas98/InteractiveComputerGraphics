from pyglet.gl import *
from pyglet.window import key
import numpy as np
import math

height = 500
width = 500
window = pyglet.window.Window(height, width)
vertex = []
points = []
draw = False
t = 0

@window.event
def on_mouse_press(x, y, button, modifiers):
    global draw
    global vertex

    if draw == False:
        v = np.array([x, y, 0])
        vertex.append(v)

@window.event
def on_key_press(symbol, modifiers):
    global draw
    global vertex

    if draw == False and symbol == key.ENTER:
        if len(vertex) < 3:
            print("You must enter at least 3 vertex.")
            vertex.clear()
        else:
            Brezier()
            draw = True

@window.event
def on_draw():
    global draw
    global vertex
    global width

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if draw == True:
        for i in range(0, len(vertex) - 1):
            glBegin(GL_LINES)
            glColor3f(1.0, 0.0, 0.0)
            glVertex2i(vertex[i][0], vertex[i][1])
            glVertex2i(vertex[i + 1][0], vertex[i + 1][1])
            glEnd()

        for i in range (len(points) - 1):
            glBegin(GL_POINTS)
            glColor3f(0.0, 0.0, 0.0)
            glVertex3f(float(points[i][0]), float(points[i][1]), float(points[i][2]))
            glVertex3f(float(points[i + 1][0]), float(points[i + 1][1]), float(points[i + 1][2]))
            glEnd() 

def Brezier():
    global vertex
    global t
    n = len(vertex) - 1
    while (t <= 1):
        point_x, point_y, point_z = 0, 0, 0
        for i in range(len(vertex)):
            vertex_x = float(vertex[i][0])
            vertex_y = float(vertex[i][1])
            vertex_z = float(vertex[i][2])
            b = math.factorial(n) / (math.factorial(i) * math.factorial(n-i))
            b = b * (t**i) * ((1-t)**(n-i))
            point_x += vertex_x * b
            point_y += vertex_y * b
            point_z += vertex_z * b
        points.append((point_x, point_y, point_z))
        t += 0.01

if __name__ == '__main__':
    pyglet.app.run()