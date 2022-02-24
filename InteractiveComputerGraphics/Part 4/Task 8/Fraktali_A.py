from pyglet.gl import *
import math

height = 800
width = 600
window = pyglet.window.Window(height, width)

epsilon = 100
m = 16
Umin, Umax = -2, 0.25
Vmin, Vmax = -1, 1
Xmax, Ymax = 800, 600

@window.event
def on_draw():
    glBegin(GL_POINTS)
    for xo in range(0, Xmax):
        for yo in range(0, Ymax):
            uo = (Umax - Umin) * xo / Xmax + Umin
            vo = (Vmax - Vmin) * yo / Ymax + Vmin
            if xo == 453 and yo == 172:
                f = 0
            r = 0
            k = -1
            c = complex(uo, vo)
            z = complex(0, 0)
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