#-*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import os


def readgraph(x):
    g = nx.read_gpickle(x)
    return g


def wmatrix(gph):
    A = nx.adjacency_matrix(gph)
    W = A.toarray()
    W = W.astype(float)
    peso_max = np.amax(W)
    W = W / peso_max
    return W

def degmatrix(W):
    tam = W.shape[0]
    d = np.zeros((tam, 1))
    I = np.identity(tam)
    for i in range(tam):
        for j in range(tam):
            d[i] = d[i] + W[i, j]
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
        W = wmatrix(G)
        D = degmatrix(W)
        gL = graphLaplacian(W, D)
        print "Diagonalizing... \n"
        PHY, LANDA = eigen(gL)
        print "Projecting eigenvectors... \n"
        eigenProjection = np.empty((0,len(W)))
        for j in range(len(PHY)):
            eigenProjection = np.vstack((eigenProjection, np.dot(PHY[j], W)))
            print "Projected eigenvector (" + str(j + 1) + "/"+ str(len(PHY)) + ")"
        wName = '/home/enrique/Proyectos/RSNs/Data/DS01216/Wmatrix/Wmat_' + name + '.csv'
        projName = '/home/enrique/Proyectos/RSNs/Data/DS01216/EigenProjection/eigenProjection_' + name + '.csv'
        np.savetxt(wName, W, delimiter=',')
        np.savetxt(projName, eigenProjection, delimiter=',')
        print "Data saved"

