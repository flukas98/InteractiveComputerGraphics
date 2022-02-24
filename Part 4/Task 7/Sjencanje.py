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
viewFactor = 0.5

velicina_x, velicina_y, velicina_z = 0.0, 0.0, 0.0  #raspon objekta po koordinatama
srediste_x, srediste_y, srediste_z = 0.0, 0.0, 0.0  #stediste objekta po koordinatama

ociste = []
glediste = []
izvor = []

ociste_radniProstor = []
glediste_radniProstor = []
izvor_radniProstor = []

vrhovi = []
vrhoviURadnomProstoru = []
normaleVrhova = []

#mnozenje sa T i P matricama
projiciraniVrhovi = []

#slika u sredini
skaliraniVrhovi = []
translatiraniVrhovi = []

trokuti = []
tezistaTrokuta = []
normaleTrokuta = []
prednjiTrokut = []

T = []
P = []

i_a, k_a, i_i, k_d = 1, 0.5, 0.7, 0.9

i_g = i_a * k_a

i_d_trokut = []
i_d_vrh = []

sjencajVrhove = True

@window.event
def on_draw():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if sjencajVrhove == True:
        for index in range (len(trokuti)):
            trokut = trokuti[index]
            if prednjiTrokut[index] == 1:
                i, j, k = trokut
                vrhoviTrokuta = [translatiraniVrhovi[i-1], translatiraniVrhovi[j-1], translatiraniVrhovi[k-1]]

                glBegin(GL_TRIANGLES)
                intenzitet = (i_d_vrh[i - 1] + i_g)
                glColor3f(intenzitet, 0.0, 0.0)
                glVertex3f(vrhoviTrokuta[0][0], vrhoviTrokuta[0][1], vrhoviTrokuta[0][2])

                intenzitet = (i_d_vrh[j - 1] + i_g)
                glColor3f(intenzitet, 0.0, 0.0)
                glVertex3f(vrhoviTrokuta[1][0], vrhoviTrokuta[1][1], vrhoviTrokuta[1][2])

                intenzitet = (i_d_vrh[k - 1] + i_g)
                glColor3f(intenzitet, 0.0, 0.0)
                glVertex3f(vrhoviTrokuta[2][0], vrhoviTrokuta[2][1], vrhoviTrokuta[2][2])
                glEnd()
    else:
        for index in range (len(trokuti)):
            trokut = trokuti[index]
            if prednjiTrokut[index] == 1:
                i, j, k = trokut
                vrhoviTrokuta = [translatiraniVrhovi[i-1], translatiraniVrhovi[j-1], translatiraniVrhovi[k-1]]

                glBegin(GL_TRIANGLES)
                intenzitet = (i_d_trokut[index] + i_g)
                glColor3f(intenzitet, 0.0, 0.0)
                glVertex3f(vrhoviTrokuta[0][0], vrhoviTrokuta[0][1], vrhoviTrokuta[0][2])
                glVertex3f(vrhoviTrokuta[1][0], vrhoviTrokuta[1][1], vrhoviTrokuta[1][2])
                glVertex3f(vrhoviTrokuta[2][0], vrhoviTrokuta[2][1], vrhoviTrokuta[2][2])
                glEnd()

@window.event
def on_key_press(symbol,modifiers):
    global sjencajVrhove
    if symbol == key.ENTER:
        sjencajVrhove = not sjencajVrhove

def SmijestanjeTijelaURadniProstor():
    global velicina_x
    global velicina_y
    global velicina_z
    
    global srediste_x
    global srediste_y
    global srediste_z

    max_velicina = max(velicina_x, velicina_y, velicina_z)
    skaliranjeURadniProstor = 2 / max_velicina

    for vrh in vrhovi:
        vrhoviURadnomProstoru.append(((vrh[0] - srediste_x) * skaliranjeURadniProstor, (vrh[1] - srediste_y) * skaliranjeURadniProstor, (vrh[2] - srediste_z) * skaliranjeURadniProstor, 1))

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
    global vrhoviURadnomProstoru
    global projiciraniVrhovi
    global T
    global P

    projiciraniVrhovi = []
    for vrh in vrhoviURadnomProstoru:
        projiciraniVrh = np.matmul(np.matmul(vrh, T), P)
        if(projiciraniVrh[3] != 0):
            projiciraniVrh = projiciraniVrh / projiciraniVrh[3]
        projiciraniVrhovi.append(projiciraniVrh)

    SkalirajNaSredisteEkrana()

def SkalirajNaSredisteEkrana():
    global projiciraniVrhovi
    global skaliraniVrhovi
    global translatiraniVrhovi

    scaleX = viewFactor * width / 2 
    scaleY = viewFactor * height / 2

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

def OdredivanjeNormalaTrokutaIPrednjihTrokuta():
    global vrhoviURadnomProstoru
    global normaleTrokuta
    global tezisniceTrokuta

    for trokut in trokuti:
        i, j, k = trokut
        vrhoviTrokuta = [vrhoviURadnomProstoru[i-1], vrhoviURadnomProstoru[j-1], vrhoviURadnomProstoru[k-1]]

        vrh_0 = np.array([vrhoviTrokuta[0][0], vrhoviTrokuta[0][1], vrhoviTrokuta[0][2]])
        vrh_1 = np.array([vrhoviTrokuta[1][0], vrhoviTrokuta[1][1], vrhoviTrokuta[1][2]])
        vrh_2 = np.array([vrhoviTrokuta[2][0], vrhoviTrokuta[2][1], vrhoviTrokuta[2][2]])
        vrh_10 = vrh_1 - vrh_0
        vrh_20 = vrh_2 - vrh_1
        normala = np.cross(vrh_10, vrh_20)
        normaleTrokuta.append(normala)

        centar_x = (vrh_0[0] + vrh_1[0] + vrh_2[0]) / 3
        centar_y = (vrh_0[1] + vrh_1[1] + vrh_2[1]) / 3
        centar_z = (vrh_0[2] + vrh_1[2] + vrh_2[2]) / 3
        tezisteTrokuta = np.array([centar_x, centar_y, centar_z])
        tezistaTrokuta.append(tezisteTrokuta)

        ociste_radniProstor = np.array([ociste[0], ociste[1], ociste[2]])
        centar_oko_vektor = ociste_radniProstor - tezisteTrokuta
        cos = np.matmul(normala, centar_oko_vektor) / (la.norm(normala) * la.norm(centar_oko_vektor))
        if cos > 0:
            prednjiTrokut.append(1)
        else:
            prednjiTrokut.append(0)
    
def OdredivanjeNormalaVrhova():
    global normaleVrhova

    for i in range (len(vrhoviURadnomProstoru)):
        vrh_index = i + 1

        normalePrilezecihTrokuta = []
        for j in range (len(trokuti)):
            trokut = trokuti[j]
            if trokut[0] == vrh_index or trokut[1] == vrh_index or trokut[2] == vrh_index:
                normalePrilezecihTrokuta.append(np.array(normaleTrokuta[j]))

        suma_x, suma_y, suma_z = 0, 0, 0
        for normalaPrilezecegTrokuta in normalePrilezecihTrokuta:
            normiranaNormalaPrilezecegTrokuta = normalaPrilezecegTrokuta / (la.norm(normalaPrilezecegTrokuta))
            suma_x += normiranaNormalaPrilezecegTrokuta[0]
            suma_y += normiranaNormalaPrilezecegTrokuta[1]
            suma_z += normiranaNormalaPrilezecegTrokuta[2]

        normalaVrha = np.array([suma_x, suma_y, suma_z]) / len(normalePrilezecihTrokuta)
        normaleVrhova.append(normalaVrha / la.norm(normalaVrha))

def AmbijentnaIDifuznaKomponentaTrokuta():
    global i_d_trokut

    for i in range (len(normaleTrokuta)):
        L = izvor_radniProstor - tezistaTrokuta[i]  # L - vektor izvorSvijetla-tezisteTrokuta
        L = L / la.norm(L)

        N = normaleTrokuta[i]          # N - vektor normalaTrokuta
        N = N / la.norm(normaleTrokuta[i])                                                                                      
                                                                                                                                
        LN = np.matmul(L, N)
        if LN < 0:
            i_d_trokut.append(0)
        else:
            i_d_trokut.append(i_i * k_d * LN)

def AmbijentnaIDifuznaKomponentaVrhova():
    global i_d_vrh

    for i in range (len(normaleVrhova)):
        L = izvor_radniProstor - np.array([vrhoviURadnomProstoru[i][0], vrhoviURadnomProstoru[i][1], vrhoviURadnomProstoru[i][2]])
        L = L / la.norm(L)

        N = normaleVrhova[i]                                               
        N = N / la.norm(normaleVrhova[i])                                                                                      
                                                                                                                                
        LN = np.matmul(L, N)
        if LN < 0:
            i_d_vrh.append(0)
        else:
            i_d_vrh.append(i_i * k_d * LN)

if __name__ == '__main__':
    ociste_glediste = open("PATH/ociste_glediste_izvor.txt", "r")		#ENTER PATH
    objekt = open("PATH/kocka.obj.txt", "r")							#ENTER PATH

    red = ociste_glediste.readlines()
    ociste = np.array([float(red[0].split()[0]), float(red[0].split()[1]), float(red[0].split()[2]), 1])
    ociste_radniProstor = np.array([float(red[0].split()[0]), float(red[0].split()[1]), float(red[0].split()[2])])

    glediste = np.array([float(red[1].split()[0]), float(red[1].split()[1]), float(red[1].split()[2]), 1])
    glediste_radniProstor = np.array([float(red[1].split()[0]), float(red[1].split()[1]), float(red[1].split()[2])])

    izvor = np.array([float(red[2].split()[0]), float(red[2].split()[1]), float(red[2].split()[2]), 1])
    izvor_radniProstor = np.array([float(red[2].split()[0]), float(red[2].split()[1]), float(red[2].split()[2])])

    xmax = sys.float_info.min
    xmin = sys.float_info.max
    ymax = sys.float_info.min
    ymin = sys.float_info.max
    zmax = sys.float_info.min
    zmin = sys.float_info.max

    for line in objekt:
        if line.startswith('v'):
            red = line.split()
            x = float(red[1])
            y = float(red[2])
            z = float(red[3])
            vrhovi.append(np.array([x, y, z]))
            if x > xmax:
                xmax = x
            if x < xmin:
                xmin = x
            if y > ymax:
                ymax = y
            if y < ymin:
                ymin = y
            if z > zmax:
                zmax = z
            if z < zmin:
                zmin = z
        if line.startswith('f'):
            red = line.split()
            trokuti.append((int(red[1]), int(red[2]), int(red[3])))

    velicina_x = xmax - xmin
    velicina_y = ymax - ymin
    velicina_z = zmax - zmin

    srediste_x = (xmax + xmin) / 2
    srediste_y = (ymax + ymin) / 2
    srediste_z = (zmax + zmin) / 2

    SmijestanjeTijelaURadniProstor()
    TransformacijaPogleda()
    PerspektivnaProjekcija()
    ProjekcijaVrhova()

    OdredivanjeNormalaTrokutaIPrednjihTrokuta()
    AmbijentnaIDifuznaKomponentaTrokuta()

    OdredivanjeNormalaVrhova()
    AmbijentnaIDifuznaKomponentaVrhova()

    pyglet.app.run()
