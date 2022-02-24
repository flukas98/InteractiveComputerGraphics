from pyglet.gl import *
import math

height = 400
width = 300
window = pyglet.window.Window(height, width)

epsilon = 100
m = 16*4
Umin, Umax = -1, 1
Vmin, Vmax = -1.2, 1.2
Xmax, Ymax = height, width

@window.event
def on_draw():
    glBegin(GL_POINTS)
    for xo in range(0, Xmax):
        for yo in range(0, Ymax):
            uo = (Umax - Umin) * (xo) / Xmax + Umin
            vo = (Vmax - Vmin) * (yo) / Ymax + Vmin
            
            r = 0
            k = -1
            c = complex(0.32, 0.043)
            z = complex(uo, vo)
            while(r <= epsilon and k <= m):
                k += 1
                zreal = z.real**2 - z.imag**2 + c.real
                zim = 2*z.real*z.imag + c.imag
                
                z = complex(zreal, zim)
                
                r = z.real**2 + z.imag**2
                r = math.sqrt(r)
            glColor3f(k / m, 1.0 - k * k / (m * m), 0.8 - k / (m * m))
            glVertex2f(xo, yo)
    glEnd()

if __name__ == '__main__':
    pyglet.app.run()