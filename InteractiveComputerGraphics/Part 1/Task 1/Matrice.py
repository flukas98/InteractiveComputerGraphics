import numpy as np
from numpy import linalg as la

#################Zadatak_1#################

#VEKTORI
a = np.array([2,3,-4])
b = np.array([-1,4,-1])
c = np.array([2, 2, 4])

v1 = a + b                       #v1 = zbroj
s = np.dot(v1, b)                #s  = skalarni umnozak
v2 = np.cross(v1, c)             #v2 = vektorski umnozak
v3 = v2 / (la.norm(v2))          #v3 = jedinicni vektor, kolinearan sa v2
v4 = -v2                         #v4 = suprotni vektor

print()
print("-----------------ZADATAK_1-----------------")
print()
print("Vektor 'a': ", a)
print("Vektor 'b': ", b)
print("Vektor 'c': ", c)
print()
print("Zbroj 'a' i 'b', v1:              ", v1)
print("Skalarni umnozak 'v1' i 'b', s:   ", s)
print("Vektorski umnozak 'v1' i 'c', v2: ", v2)
print("Jedinicni vektor 'v2', v3:        ", v3)
print("Suprotni vektor 'v2', v4:         ", v4)
print("-------------------------------------------")

#MATRICE
m1 = np.array([[1, 2, 3], [2, 1, 3], [4, 5, 1]])
m2 = np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])

M1 = m1 + m2                        #M1 = zbroj matrica
M2 = np.matmul(m1, m2.transpose())  #M2 = umnozak, transponirana matrica
M3 = np.matmul(m1, la.inv(m2))      #M3 = umnozak, inverzna matrica


print()
print("Matrica 'm1': ")
print(m1)
print("Matrica 'm2': ")
print(m2)
print()
print("Zbroj 'm1' i 'm2', M1: ")
print(M1)
print("Umnozak 'm1' i 'm2^T', M2: ")
print(M2)
print("Umnozak 'm1' i 'm2^(-1)', M3: ")
print(M3)

#################Zadatak_2#################

print()
print("-----------------ZADATAK_2-----------------")
print()
A = np.arange(9)
A.shape = (3, 3)
B = np.arange(3)
B.shape = (3, 1)

for i in range(3):
    for j in range(3):
        A[i,j] = input()
    B[i,0] = input()
    
x = la.solve(A, B)
x.shape = (1, 3)

print(x)

#################Zadatak_3#################

print()
print("-----------------ZADATAK_3--------------------")
print()

A = np.arange(9)
A.shape = (3, 3)
T = np.arange(3)
T.shape = (3, 1)

for j in range(3):
    for i in range(3):
        A[i,j] = input()
        
for i in range(3):
    T[i,0] = input()
    
t = np.matmul(la.inv(A), T)

print(t)
