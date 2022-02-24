import numpy as np
import sys
from numpy import linalg as la
from pyglet.gl import *

height = 500
width = 500
cCenterX = width/2
cCenterY = height/2
centerX = 0
centerY = 0
window = pyglet.window.Window(height, width)
vertex = []
vertexScaled = []
vertexTranslated = []
polygons = []
originalCoefs = []
translatedCoefs = []
skaliranje = 300
translacija = 0
viewFactor = 0.8
scale = 1

@window.event
def on_draw():
    global vertexTranslated
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    for polygon in polygons:
        k1, k2, k3 = polygon
        glBegin(GL_LINE_LOOP)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f((vertexTranslated[k1 - 1][0]), (vertexTranslated[k1 - 1][1]), 0)
        glVertex3f((vertexTranslated[k2 - 1][0]), (vertexTranslated[k2 - 1][1]), 0)
        glVertex3f((vertexTranslated[k3 - 1][0]), (vertexTranslated[k3 - 1][1]), 0)
        glEnd()
    
def planeCoefs(polygon):
    global vertex
    global vertexTranslated

    k1, k2, k3 = polygon[0], polygon[1], polygon[2]
    
    v1 = vertex[k1 - 1]
    v2 = vertex[k2 - 1]
    v3 = vertex[k3 - 1]
    v = [v1, v2, v3]

    A = (v[1][1]-v[0][1])*(v[2][2]-v[0][2]) - (v[1][2]-v[0][2])*(v[2][1]-v[0][1])
    B = (v[1][0]-v[0][0])*(v[2][2]-v[0][2])*(-1) + (v[1][2]-v[0][2])*(v[2][0]-v[0][0])
    C = (v[1][0]-v[0][0])*(v[2][1]-v[0][1]) - (v[1][1]-v[0][1])*(v[2][0]-v[0][0])
    D = (-1)*v[0][0]*A - v[0][1]*B - v[0][2]*C

    v1t = vertexTranslated[k1 - 1]
    v2t = vertexTranslated[k2 - 1]
    v3t = vertexTranslated[k3 - 1]
    vt = [v1t, v2t, v3t]

    At = (vt[1][1]-vt[0][1])*(vt[2][2]-vt[0][2]) - (vt[1][2]-vt[0][2])*(vt[2][1]-vt[0][1])
    Bt = (vt[1][0]-vt[0][0])*(vt[2][2]-vt[0][2])*(-1) + (vt[1][2]-vt[0][2])*(vt[2][0]-vt[0][0])
    Ct = (vt[1][0]-vt[0][0])*(vt[2][1]-vt[0][1]) - (vt[1][1]-vt[0][1])*(vt[2][0]-vt[0][0])
    Dt = (-1)*vt[0][0]*At - vt[0][1]*Bt - vt[0][2]*Ct

    return A, B, C, D, At, Bt, Ct, Dt

def pointObjectRelation(point):
    x = point[0]
    y = point[1]
    z = point[2]
    outside = 0
    on = 0
    
    for i in range (len(originalCoefs)):
        a = originalCoefs[i][0]
        b = originalCoefs[i][1]
        c = originalCoefs[i][2]
        d = originalCoefs[i][3]
        check = a*x + b*y + c*z + d
        if(check > 0):
            outside = 1
        if(check == 0):
            on = 1
        
    if (outside == 1):
        print("Point is outside of the original object.")
    elif (outside == 0 and on == 1):
        print("Point is on the original object.")
    else:
        print("Point is inside of the original object.")

    outside = 0
    on = 0
    for i in range (len(translatedCoefs)):
        a = translatedCoefs[i][0]
        b = translatedCoefs[i][1]
        c = translatedCoefs[i][2]
        d = translatedCoefs[i][3]
        check = a*x + b*y + c*z + d
        if(check > 0):
            outside = 1
        if(check == 0):
            on = 1
        
    if (outside == 1):
        print("Point is outside of the translated object.")
    elif (outside == 0 and on == 1):
        print("Point is on the translated object.")
    else:
        print("Point is inside of the translated object.")

if __name__ == '__main__':
    obj = open("PATH/porsche.obj.txt", "r")		#ENTER PATH

    xmax = sys.float_info.min
    xmin = sys.float_info.max
    ymax = sys.float_info.min
    ymin = sys.float_info.max
    
    for line in obj:
        if line.startswith("v"):
            XX, x, y, z = line.split()
            x = float(x) 
            y = float(y)
            z = float(z)
            if (x > xmax):
                xmax = x
            if (x < xmin):
                xmin = x
            if (y > ymax):
                ymax = y
            if (y < ymin):
                ymin = y
            vertex.append((x, y, z))
        elif line.startswith("f"):
            XX, v1, v2, v3 = line.split()
            polygons.append((int(v1), int(v2), int(v3)))

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

    for v in vertex:
        x = v[0]*scale
        y = v[1]*scale
        z = v[2]*scale
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
        vertexScaled.append((x, y, z))

    centerX = (xmax + xmin)/2
    centerY = (ymax + ymin)/2

    transX = cCenterX - centerX
    transY = cCenterY - centerY

    transZ = -zmin

    for v in vertexScaled:
        x = v[0] + transX
        y = v[1] + transY
        z = v[2] + transZ
        vertexTranslated.append((x, y, z))

    for i in range (0, len(polygons)):
        A, B, C, D, At, Bt, Ct, Dt = planeCoefs(polygons[i])
        originalCoefs.append((float(A), float(B), float(C), float(D)))
        translatedCoefs.append((float(At), float(Bt), float(Ct), float(Dt)))

    print("Point cordinates:")
    x = float(input("  x: "))
    y = float(input("  y: "))
    z = float(input("  z: "))
    point = (x, y, z)
    pointObjectRelation(point)

    pyglet.app.run()

