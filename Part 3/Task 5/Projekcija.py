from pyglet.gl import *
import numpy as np
from numpy import linalg as la
from pyglet.window import mouse
from pyglet.window import key
import math
import sys

height = 500
width = 500
window = pyglet.window.Window(height, width)

cCenterX = width/2
cCenterY = height/2
centerX = 0
centerY = 0
vertex = []
vertexScaled = []
vertexTranslated = []
polygons = []
skaliranje = 300
translacija = 0
viewFactor = 0.5
scale = 1

ociste = []
glediste = []
vrhovi = []
projiciraniVrhovi = []
skaliraniVrhovi = []
translatiraniVrhovi = []
trokuti = []
T = []
P = []

def TransformacijaPogleda():
    global ociste
    global glediste
    global T
    
    T1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1*ociste[0], -1*ociste[1], -1*ociste[2], 1]])

    glediste1 = np.matmul(glediste, T1)
    
    sina = glediste1[1] / math.sqrt(glediste1[0]*glediste1[0] + glediste1[1]*glediste1[1])
    cosa = glediste1[0] / math.sqrt(glediste1[0]*glediste1[0] + glediste1[1]*glediste1[1])
    T2 = np.array([[cosa, -1*sina, 0, 0], [sina, cosa, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    
    glediste2 = np.matmul(glediste1, T2)
    
    sinb = glediste2[0] / math.sqrt(glediste2[0]*glediste2[0] + glediste2[2]*glediste2[2])
    cosb = glediste2[2] / math.sqrt(glediste2[0]*glediste2[0] + glediste2[2]*glediste2[2])
    T3=np.array([[cosb, 0, sinb, 0], [0, 1, 0, 0], [-1*sinb, 0, cosb, 0], [0, 0, 0, 1]])
    
    T4=np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    T5=np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    T = np.matmul(T1, T2)
    T = np.matmul(T, T3)
    T = np.matmul(T, T4)
    T = np.matmul(T, T5)

def PerspektivnaProjekcija():
    global ociste
    global glediste
    global P

    H = np.sqrt((ociste[0] - glediste [0])**2 + (ociste[1] - glediste[1])**2 + (ociste[2] - glediste[2])**2) 
    P = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1/H], [0, 0, 0, 0]])

def ProjekcijaVrhova():
    global vrhovi
    global projiciraniVrhovi
    global T
    global P

    projiciraniVrhovi = []
    for vrh in vrhovi:
        projiciraniVrh = np.matmul(np.matmul(vrh, T), P)
        if(projiciraniVrh[3] != 0):
            projiciraniVrh = projiciraniVrh / projiciraniVrh[3]
        projiciraniVrhovi.append(projiciraniVrh)

    Skaliraj()

def Skaliraj():
    global projiciraniVrhovi
    global skaliraniVrhovi
    global translatiraniVrhovi

    skaliraniVrhovi = []
    translatiraniVrhovi = []

    xmax = sys.float_info.min
    xmin = sys.float_info.max
    ymax = sys.float_info.min
    ymin = sys.float_info.max

    for vrh in projiciraniVrhovi:
        x = float(vrh[0]) 
        y = float(vrh[1])
        z = float(vrh[2])
        if (x > xmax):
            xmax = x
        if (x < xmin):
            xmin = x
        if (y > ymax):
            ymax = y
        if (y < ymin):
            ymin = y

    objWidth = xmax - xmin
    objHeight = ymax - ymin

    scaleX = viewFactor * width / objWidth 
    scaleY = viewFactor * height / objHeight

    if scaleX > scaleY:
        scale = scaleY
    else:
        scale = scaleX

    xmax = sys.float_info.min
    xmin = sys.float_info.max
    ymax = sys.float_info.min
    ymin = sys.float_info.max
    zmin = sys.float_info.max

    for vrh in projiciraniVrhovi:
        x = vrh[0]*scale
        y = vrh[1]*scale
        z = vrh[2]*scale
        if (x > xmax):
            xmax = x
        if (x < xmin):
            xmin = x
        if (y > ymax):
            ymax = y
        if (y < ymin):
            ymin = y
        if (z < zmin):
            zmin = z
        skaliraniVrhovi.append((x, y, z))

    centerX = (xmax + xmin)/2
    centerY = (ymax + ymin)/2

    transX = cCenterX - centerX
    transY = cCenterY - centerY

    transZ = -zmin

    for vrh in skaliraniVrhovi:
        x = vrh[0] + transX
        y = vrh[1] + transY
        z = vrh[2] + transZ
        translatiraniVrhovi.append((x, y, z))

@window.event
def on_key_press(symbol,modifiers):
    global glediste
    if symbol == key.NUM_6:
        glediste = glediste[0] + 1, glediste[1], glediste[2], 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

    elif symbol == key.NUM_4:
        glediste = glediste[0] - 1, glediste[1], glediste[2], 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

    elif symbol == key.NUM_8:
        glediste = glediste[0], glediste[1] + 1, glediste[2], 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

    elif symbol == key.NUM_2:
        glediste = glediste[0], glediste[1] - 1, glediste[2], 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

    elif symbol == key.NUM_9:
        glediste = glediste[0], glediste[1], glediste[2] + 1, 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

    elif symbol == key.NUM_1:
        glediste = glediste[0], glediste[1], glediste[2] - 1, 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

@window.event        
def on_mouse_press(x, y, button, modifiers):
    global ociste

    #left button
    if (button == 1):
        ociste = ociste[0] + 1, ociste[1] + 1, ociste[2] + 1, 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

    #right button
    elif (button == 4):
        ociste = ociste[0] - 1, ociste[1] - 1, ociste[2] - 1, 1
        TransformacijaPogleda()
        PerspektivnaProjekcija()
        ProjekcijaVrhova()

@window.event
def on_draw():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    for trokut in trokuti:
        i, j, k = trokut
        vrhoviTrokuta = [translatiraniVrhovi[i-1], translatiraniVrhovi[j-1], translatiraniVrhovi[k-1]]
        glBegin(GL_LINE_LOOP)
        for vrh in vrhoviTrokuta:           
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(float(vrh[0]), float(vrh[1]), float(vrh[2]))
        glEnd()

if __name__ == '__main__':
    ociste_glediste = open("PATH/ociste_glediste.txt", "r")		#ENTER PATH
    objekt = open("PATH/kocka.obj.txt", "r")					#ENTER PATH

    red = ociste_glediste.readlines()
    ociste = float(red[0].split()[0]), float(red[0].split()[1]), float(red[0].split()[2]), 1
    glediste = float(red[1].split()[0]), float(red[1].split()[1]), float(red[1].split()[2]), 1
    
    for line in objekt:
        if line.startswith('v'):
            red = line.split()
            vrhovi.append((float(red[1]), float(red[2]), float(red[3]), 1))
        if line.startswith('f'):
            red = line.split()
            trokuti.append((int(red[1]), int(red[2]), int(red[3])))

    TransformacijaPogleda()
    PerspektivnaProjekcija()
    ProjekcijaVrhova()

    pyglet.app.run()
