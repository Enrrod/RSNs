#-*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import os


def readgraph(x):
    g = nx.read_gpickle(x)
    return g


def adjmatrix(gph):
    A = nx.adjacency_matrix(gph)
    A = A.toarray()
    A = A.astype(float)
    peso_max = np.amax(A)
    A = A / peso_max
    #A[np.where(A < thres)] = 0
    A[np.where(A > 0)] = 1
    return A

def degmatrix(A):
    tam = A.shape[0]
    d = np.zeros((tam, 1))
    I = np.identity(tam)
    for i in range(tam):
        for j in range(tam):
            d[i] = d[i] + A[i, j]
    D = I * d
    return D


def graphLaplacian(W, D):
    L = D - W
    sqD = D
    for i in range(len(sqD)):
        if sqD[i,i] != 0:
            sqD[i,i] = 1 / np.sqrt(sqD[i,i])
        else:
            sqD[i, i] = 0
    gLap = np.dot(sqD,np.dot(L,sqD))
    return gLap


def eigen(gLap):
    (LANDA, PHY) = np.linalg.eig(gLap)  # calculamos los autovalores
    tam = PHY.shape[1]
    ind = np.argsort(LANDA)  # de menor a mayor
    #ind = ind[::-1]         # de mayor a menor
    LANDA = LANDA[ind]
    for i in range(tam):
        PHY[i] = PHY[i][ind]
    return PHY.T , LANDA     # Phy ordered by rows

if __name__=="__main__":

    directory = '/home/enrique/Proyectos/RSNs/Data/DS01216/Graphs'
    subjects = os.listdir(directory)
    for i in range(len(subjects)):
        name = subjects[i][4:13]
        print "Processing subject " + name + "\n"
        graph = directory + '/' + subjects[i]
        G = readgraph(graph)
        A = adjmatrix(G)
        D = degmatrix(A)
        gL = graphLaplacian(A, D)
        print "Diagonalizing... \n"
        PHY, LANDA = eigen(gL)
        PHY, LANDA = PHY.real, LANDA.real
        print "Projecting eigenvectors... \n"
        eigenProjection = np.empty((0,len(A)))
        for j in range(len(PHY)):
            eigenProjection = np.vstack((eigenProjection, np.dot(PHY[j], A)))
            print "Projected eigenvector (" + str(j + 1) + "/"+ str(len(PHY)) + ")"
        wName = '/home/enrique/Proyectos/RSNs/Data/DS01216/umbralized/Amat/Amat_' + name + '.csv'
        projName = '/home/enrique/Proyectos/RSNs/Data/DS01216/umbralized/EigenProjection/eigenProjection_' + name + '.csv'
        np.savetxt(wName, A, delimiter=',')
        np.savetxt(projName, eigenProjection, delimiter=',')
        print "Data saved"

