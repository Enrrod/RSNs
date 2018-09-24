# -*- coding: utf-8 -*-

# -----IMPORTACIÓN DE LOS MÓDULOS NECESARIOS----------------------------------------------------------------------------

import numpy as np
import nibabel as nib

# -----DEFINICIÓN DE FUNCIONES------------------------------------------------------------------------------------------


def openAtlas(file):
    img = nib.load(file)
    data = img.get_data()
    return data


def inspectAtlas(data):
    n_roi = 16783          # número de ROIs que tiene el atlas
    roi_list = []
    for i in range(n_roi + 1):
        roi_list.append(np.empty((0,3)))
    X = data.shape[0]
    Y = data.shape[1]
    Z = data.shape[2]
    for i in range(X):
        for j in range(Y):
            for k in range(Z):
                print ("Inspeccionando coordenada" + str([i,j,k]))
                value = data[i,j,k]
                roi_list[value] = np.vstack((roi_list[value],np.array([i,j,k])))
    return roi_list


def centroids(roi_list):
    cent = np.empty((0,3))
    #bPoints = np.empty((0,3))
    n_roi = len(roi_list)
    for i in range(1,n_roi):
        cent = np.vstack((cent, np.mean(roi_list[i], axis=0)))
        #bPoints = np.vstack((bPoints, roi_list[i]))
    return cent


if __name__=="__main__":

    # Definición de la ruta del atlas

    atlasRoute = '/home/enrique/Proyectos/RSNs/Data/Atlases/DS16784.nii'

    # Calculamos los centroides

    data = openAtlas(atlasRoute)
    roi_list = inspectAtlas(data)
    cent = centroids(roi_list)
    np.savetxt('/home/enrique/Proyectos/RSNs/Data/Atlases/centroidsDS16784.csv', cent, delimiter=",")
    #np.savetxt('/home/enrique/Dropbox/TFM/grafos/bPointsDS00071.csv', bPoints, delimiter=",")
