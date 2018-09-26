# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib

def openAtlas(file):
    img = nib.load(file)
    data = img.get_data()
    return data


if __name__=="__main__":

    cents = np.genfromtxt('/home/enrique/Proyectos/RSNs/Data/Atlases/centroidsDS01216.csv', delimiter=",")
    data = openAtlas('/home/enrique/Proyectos/RSNs/Data/Atlases/Yeo2011_7Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii')

    centRSNref = np.empty((0, 4))
    for i in range(len(cents)):
        x = cents[i][0]
        y = cents[i][1]
        z = cents[i][2]
        value = data[int(round(x)), int(round(y)), int(round(z)), 0]
        centRSNref = np.vstack((centRSNref, np.array([x,y,z,value])))

    np.savetxt('/home/enrique/Proyectos/RSNs/Data/Atlases/centroidsDS01216_RSNref.csv', centRSNref, delimiter=",")
