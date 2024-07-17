# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 20:29:27 2023

@author: Victor Borrayo
"""



import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib import rcParams
import matplotlib as mpl
import numpy as np

#Vector de colores base
designC = {
    "vr" : "#9DD3A4",
    "az" : "#304059",
    "nr" : "#F56522",
    "cs" : "#3997D4",
    "gr" : "#989FAF"
    }

cnList = list(designC.keys())
bcList = list(designC.values())


dcDic = {}
dcDic2 = {}

for c, i in enumerate(cnList):
    cmap = clr.LinearSegmentedColormap.from_list('custom blue', ["#FFFFFF",designC[i],"#000000"], N=13)
    dcDic2[i] = cmap
    num_centers = 7
    start_index = (cmap.N - num_centers) // 2
    end_index = start_index + num_centers - 1
    indices = np.linspace(start_index/cmap.N, end_index/cmap.N, num_centers)
    center_colors = cmap(indices)
    cmap = clr.LinearSegmentedColormap.from_list(i, center_colors, N=len(center_colors))
    dcDic[i] = cmap
    try:
        aCmap = plt.get_cmap(name=i+'-d')
    except ValueError:
        aCmap = None
    if aCmap is None:
        mpl.cm.register_cmap(name=i+'-d', cmap=cmap)
    else:
        pass

#ccDic = {}

for c, i in enumerate(list(dcDic2.keys())):
    cmap = clr.LinearSegmentedColormap.from_list('custom blue', [dcDic2[i](2),dcDic2[i](7)], N=255)
    #aCmap = plt.get_cmap(name=i+'-c')
    try:
        
        aCmap = plt.get_cmap(name=i+'-c')
    except ValueError:
        aCmap = None
    if aCmap is None:
        mpl.cm.register_cmap(name=i+'-c', cmap=cmap)
    else:
        pass
    #ccDic[i] = cmap

# Limpiar y cerrar la figura actual antes de generar una nueva gráfica
plt.clf()
plt.close()

#%%Creando archivo con diseño básico

if __name__ == "__main__":
    


    with open("style1.mplstyle", "w") as f:

        #Estilo 1
        fresmC = designC['cs']
        fressC1 = clr.to_rgb(designC['az'])
        fressC2 = designC['gr']
        fressC2_d = plt.get_cmap('gr-d')(0)
        fressC2_d2 = plt.get_cmap('gr-d')(2)
        dDic1 = {"figure.facecolor" : "FFFFFFFF",'xtick.color': fressC2_d2, 'ytick.color': fressC2_d2, 'axes.edgecolor' : fressC2_d2,'axes.titlecolor': fressC1,\
                'axes.spines.left': True,'axes.spines.bottom': True,'axes.spines.right': False,'axes.spines.top': False}
        #Creando archivo de diseño       
        for i in dDic1.keys():
            f.write("{} : {}\n".format(i,dDic1[i]))
        f.close()





