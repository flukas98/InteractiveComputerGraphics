from pyglet.gl import *

window = pyglet.window.Window(500, 500)
x1 = 0
y1 = 0
x2 = 0
y2 = 0
draw = True

@window.event
def on_mouse_press(x, y, button, modifiers):
    global draw
    global x1, y1, x2, y2

    if draw == True:
        x1 = x
        y1 = y
        draw = False
    else:
        x2 = x
        y2 = y
        draw = True

def draw_bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):
        bresenham_draw_x(x1, y1, x2, y2)
    else:
        bresenham_draw_y(x1, y1, x2, y2)

def bresenham_draw_x(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    tan = dy*(1.0)/dx
    
    x = x1
    y = y1
    
    # 0 - 45
    if (dx >= 0 and dy >= 0):
        d = tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(dx):
            glVertex2i(x, y)
            if d > 0:
                y = y + 1
                d = d - 1
            x = x + 1
            d = d + tan
        glEnd()

    # 315 - 0    
    elif (dx >= 0 and dy <= 0):
        d = - tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(dx):
            glVertex2i(x, y)
            if d > 0:
                y = y - 1
                d = d - 1
            x = x + 1
            d = d - tan
        glEnd()

    # 135 - 180       
    elif (dx <= 0 and dy >= 0):
        d = - tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(-dx):
            glVertex2i(x, y)
            if d > 0:
                y = y + 1
                d = d - 1
            x = x - 1
            d = d - tan
        glEnd()
    
    # 180 - 225 
    elif (dx <= 0 and dy <= 0):
        d = tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(-dx):
            glVertex2i(x, y)
            if d > 0:
                y = y - 1
                d = d - 1
            x = x - 1
            d = d + tan
        glEnd()

def bresenham_draw_y(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    tan = dx*1.0/dy
    
    x = x1
    y = y1
    
    # 45 - 90
    if (dx >= 0 and dy >= 0):
        d = tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(dy):
            glVertex2i(x, y)
            if d > 0:
                x = x + 1
                d = d - 1
            y = y + 1
            d = d + tan
        glEnd()
    
    # 270 - 315
    elif (dx >= 0 and dy <= 0):
        d = - tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(-dy):
            glVertex2i(x, y)
            if d > 0:
                x = x + 1
                d = d - 1
            y = y - 1
            d = d - tan
        glEnd()
    
    # 90 - 135
    elif (dx <= 0 and dy >= 0):
        d = - tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(dy):
            glVertex2i(x, y)
            if d > 0:
                x = x - 1
                d = d - 1
            y = y + 1
            d = d - tan
        glEnd()
    
    # 225 - 270
    elif (dx <= 0 and dy <= 0):
        d = tan - 0.5
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(-dy):
            glVertex2i(x, y)
            if d > 0:
                x = x - 1
                d = d - 1
            y = y - 1
            d = d + tan
        glEnd()

@window.event
def on_draw():
    global draw

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    if draw == True:
        offset = 0
        dx = x2 - x1
        if(dx != 0):
            draw_bresenham(x1, y1, x2, y2)
            offset = 20
        glBegin(GL_LINES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex2i(x1, y1 + offset)  # crtanje gotove linije
        glVertex2i(x2, y2 + offset)
        glEnd()

if __name__ == '__main__':
    pyglet.app.run()
