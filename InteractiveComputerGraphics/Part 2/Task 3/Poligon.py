from pyglet.gl import *
from pyglet.window import key
import numpy as np

height = 500
width = 500
window = pyglet.window.Window(height, width)
vertex = []
edges = []
counter = 0
draw = False

@window.event
def on_mouse_press(x, y, button, modifiers):
    global draw
    global counter
    global vertex
    global edges

    if draw == False:
        v = np.array([x, y, 1])
        vertex.append(v)
        print(vertex[counter]) 
        if counter != 0:
            y1 = vertex[counter - 1][1]
            y2 = vertex[counter][1]
            edge = np.cross(vertex[counter - 1], vertex[counter])
            if y1 > y2:
                e = (edge, "R")
                edges.append(e)
            else:
                e = (edge, "L")
                edges.append(e)
        counter += 1
    else:
        on = False
        out = False

        X = np.array([x, y, 1])
        for i in range(0, len(edges)):
            dotCheck = np.dot(X, edges[i][0])
            if dotCheck == 0:
                on = True
            elif dotCheck > 0:
                out = True

        if on == True:
            print("X is on polygon.")
        elif out == True:
            print("X is outside polygon.")
        else:
            print("X is inside polygon.")

@window.event
def on_key_press(symbol, modifiers):
    global draw
    global vertex
    global edges
    global counter

    if draw == False and symbol == key.ENTER:
        if len(vertex) < 3:
            print("You must enter at least 3 vertex.")
        else:
            y1 = vertex[counter - 1][1]
            y2 = vertex[0][1]
            edge = np.cross(vertex[counter - 1], vertex[0])
            if y1 > y2:
                e = (edge, "R")
                edges.append(e)
            else:
                e = (edge, "L")
                edges.append(e)
            isValid = True
            n = len(vertex)
            for i in range(1, n + 1):
                if i <= n - 2:
                    j = i + 2
                else:
                    j = i + 2 - n
                
                v = vertex[j - 1]
                b = edges[i - 1][0]
                validation = np.dot(v, b)
                if validation >= 0:
                    isValid = False
                    break
            if isValid == False:
                print("Polygon is not convex or it is entered CW, enter again.")
                vertex.clear()
                edges.clear()
                counter = 0
            else:
                draw = True

@window.event
def on_draw():
    global draw
    global vertex
    global edges
    global width

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if draw == True:
        y = []
        
        for i in range(0, len(vertex)):
            y.append(vertex[i][1])
            glBegin(GL_LINES)
            glColor3f(1.0, 0.0, 0.0)
            if i != len(vertex) - 1:
                glVertex2i(vertex[i][0], vertex[i][1])
                glVertex2i(vertex[i + 1][0], vertex[i + 1][1])
            else:
                glVertex2i(vertex[i][0], vertex[i][1])
                glVertex2i(vertex[0][0], vertex[0][1])
            glEnd()

        ymax = max(y)
        ymin = min(y)

        for i in range(ymin, ymax + 1):
            Lmax = 0
            Dmin = width
            for j in range(0, len(edges)):
                yp = [0, 1, -i]
                crossH3 = np.cross(edges[j][0], yp)
                crossN2 = [int(crossH3[0]/crossH3[2]), int(crossH3[1]/crossH3[2]), 1]
                if edges[j][1] == "L":
                    if crossN2[0] > Lmax:
                        Lmax = crossN2[0]
                if edges[j][1] == "R":
                    if crossN2[0] < Dmin:
                        Dmin = crossN2[0]
            glBegin(GL_LINES)
            glColor3f(1.0, 0.0, 0.0)
            glVertex2i(Lmax, i)
            glVertex2i(Dmin, i)
            glEnd()

        

if __name__ == '__main__':
    pyglet.app.run()