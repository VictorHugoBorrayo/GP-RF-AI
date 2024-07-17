# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:09:33 2022

@author: Victor Borrayo
"""

from scipy import constants
import sys
import os
sys.path.append('../../../')
import warnings
import json
import requests
import math
import matplotlib as mpl
from matplotlib.patches import Ellipse
import numpy as np
from Python.Style.styles import  *
from Python.Private.constants import elevation_api_k1
from matplotlib import pyplot as plt1

#%%
#ffFlag = True

#%%Funciones
def cord2dis(cDic):
    lat1 = np.deg2rad(cDic['lat1'])
    lon1 = np.deg2rad(cDic['lon1'])
    lat2 = np.deg2rad(cDic['lat2'])
    lon2 = np.deg2rad(cDic['lon2'])
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    R = 6373.0
    a = math.sin(dlat / 2)**2 + math.cos(lat2) * math.cos(lat1) * math.sin(dlon / 2)**2
    dist = R *2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return dist * 1000

def cord2disV2(lat1,lon1,lat2,lon2):
    try:
        lat1 = np.deg2rad(lat1)
        lon1 = np.deg2rad(lon1)
        lat2 = np.deg2rad(lat2)
        lon2 = np.deg2rad(lon2)
        dlat = lat1 - lat2
        dlon = lon1 - lon2
        R = 6373.0
        a = math.sin(dlat / 2)**2 + math.cos(lat2) * math.cos(lat1) * math.sin(dlon / 2)**2
        dist = R *2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return dist * 1000
    except:
        return np.nan


def pathCreator(cDic,n):
    #latitude array
    if cDic["lat1"] != cDic["lat2"]:
        laPs = np.linspace(cDic["lat1"],cDic["lat2"],n)
    else:
        laPs =  [cDic["lat1"]]*n
    #longitude array
    if cDic["lon1"] != cDic["lon2"]:
        loPs = np.linspace(cDic["lon1"],cDic["lon2"],n)
    else:
        loPs =  [cDic["lon1"]]*n
    #Path generation
    path = [[round(laPs[i],6),round(loPs[i],6)] for i in range(n)]
    return path


def getElevation(path):
    url2 = "https://maps.googleapis.com/maps/api/elevation/json?locations={}&key=" + elevation_api_k1
    locString = ""
    payload={}
    headers = {}
    for c, i in enumerate(path):
        if c!= len(path)-1:
            locString = locString + str(i[0]) + "," + str(i[1]) +"|"
        else:
            locString = locString + str(i[0]) + "," + str(i[1])
    response = requests.request("GET", url2.format(locString), headers=headers, data=payload)
    tVec = eval(response.text)["results"]
    eVec = []
    rVec = []
    for i in tVec:
        eVec.append(i['elevation'])
        rVec.append(i['resolution'])
    return eVec, rVec


def getDist(path):
    distVec = [0]
    for i in range(1,len(path)):
        distVec.append(cord2dis({'lat1':path[0][0],'lon1':path[0][1],'lat2':path[i][0],'lon2':path[i][1]}))
    return distVec



def fresnelObstruction(tdown,tup,tel,csize):
    if tel<tdown:
        return 0
    elif tel>tup:
        return 1
    else:
        try:
            t0 = tel - tdown
            po = t0/(2*csize)
            return round(po,2)
        except ZeroDivisionError:
            if tup < tel:
                return 1
            else:
                return 0


fresnelOVec = np.vectorize(fresnelObstruction)




#def getFresnelObstruction(cE, ):
    



#%%Desarollo



#, eVec, rVec

#mpl.rcParams['axes.spines.right'] = True
#mpl.rcParams['axes.spines.top'] = True


#Diseño base
fresmC = designC['cs']
fressC1 = designC['az']
fressC2 = designC['gr']
fressC2_d = plt.get_cmap('gr-d')(0)
fressC2_d2 = plt.get_cmap('gr-d')(2)


#Función de análisis Fresnel
def fresnelAnalysis(lnkDic, n, fPlot = False):#eVec, rVec
    #Configurando gráfica
    #CALCULOS
    path = pathCreator(lnkDic, n)
    eVec, rVec = getElevation(path)
    distVec = getDist(path)
    #Fresnel analysis variables
    b0 = eVec[0] + lnkDic['h1']
    h2 = eVec[-1] + lnkDic['h2']
    f = lnkDic['freq']
    deltaH = b0 - h2
    Dalt = distVec[-1]
    De = math.sqrt(Dalt**2 + deltaH**2)
    beta = math.atan(-deltaH/Dalt)
    #b = math.sqrt((De*constants.speed_of_light)/(4*f))
    b = 1/2 * math.sqrt(constants.speed_of_light*De/f)
    m = -deltaH/Dalt
    Xc = Dalt/2
    lEq = lambda xi: m*(xi) + b0
    veclEq = np.vectorize(lEq)
    Yc = lEq(Xc)
    #Yc = m*(Xc) + eVec[0] + lnkDic['h1']
    Cf = De/2
    a = math.sqrt(Cf**2 + b**2)
    ay = a * math.sin(beta)
    ax = a * math.cos(beta)
    #Calculo de puntos críticos
    yiVec = veclEq(distVec)
    diEq = np.vectorize(lambda xi: math.sqrt(xi**2 + (b0-lEq(xi))**2))
    hdiEq = np.vectorize(lambda di: math.sqrt((di*(De-di)*constants.speed_of_light)/(De*f)))        
    tdiVec = diEq(distVec)
    hdiVec = hdiEq(tdiVec)
    yhdiVec = hdiVec * math.cos(beta)
    restVec = -tdiVec + De
    downP = yiVec - yhdiVec
    upP = yiVec + yhdiVec
    
    hmx = np.max([b0,h2,np.max(eVec)])
    hmin = np.min([b0,h2,np.min(eVec)])
    hn = hmx-hmin
    
    yMins = [hmin - hn*0.05]*n
    cpVec = eVec.copy()
    cpVec[0] = b0
    cpVec[-1] = h2    
    #Obstrucción de la zona de Fresnel
    obVec = fresnelOVec(downP,upP,cpVec, yhdiVec)
    if fPlot:
        #Importando diseño
        #if ffFlag:
        #plt1.style.use('../Python/Style/style1.mplstyle')
        #    ffFlag = False
        #PLOT
        #Reajustando a un máximo de 10 etiquetas en visualización
        arr = np.linspace(0,n-1,10, dtype = int)
        tarr = [distVec[i] for i in arr]
        #Torres
        torresD = [distVec[i] for i in [0,-1]]
        torresMin = [eVec[i] for i in [0,-1]]
        torresMax = [b0,h2]
        #Creando figura
        cplot = plt1.figure()
        ax = cplot.gca()
        #Tamaño de márgenes
        plt1.xlim(-De*0.09,Dalt*1.09)
        #plt.ylim(hmin - hn*0.05,hmx + hn *0.2)#
        #Inicio ploteo
        ax.plot(distVec,eVec, markersize = 5, color = fressC2_d)
        fresEllips = Ellipse(xy = (Xc,Yc), fill = False, width = 2*a, height = 2*b, angle = math.degrees(beta), color = fressC2_d)
        plt1.vlines(torresD,torresMin,torresMax, color = fressC2)
        ax.add_patch(fresEllips)
        plt1.vlines(distVec,yMins,eVec, color = fresmC)
        #Creado anotaciones con valores de Característica Fresnel
        stp = De/n
        lEq2 = lambda xi: m*(xi) + b0*1.08
        ystp = np.max(yhdiVec)
        for count, i in enumerate(obVec):
            cx = distVec[count]# + stp*0.4
            cy = cpVec[count] + ystp*0.3
            #cy = eVec[count] * 1.001
            if count in arr:
                plt1.annotate(format(i,'.2f'),(cx,cy), ha='center', color = fressC1, fontsize = 10)
        #Ajustando tamaño de letra en eje x
        if De>2000:
            ax.tick_params(axis='x', which='major', labelsize=8)
        #Modficiando tamaño de eje vertical
        plt1.ylim(hmin - hn*0.05,ax.get_yticks()[-1])
        #Configuración final
        plt1.xticks(ticks = distVec)
        plt1.xticks(ticks = tarr)
        plt1.title("Característica Fresnel")
        import os
        cwd = os.getcwd()
        plt1.savefig(os.path.join(cwd, 'Fresnel_Feature.jpg'), dpi = 300)
        #Configurando color de margen
        plt1.rcParams['figure.facecolor'] = 'FFFFFFFF'
        plt1.show()
        #return ax
    return obVec, distVec, eVec


#Función de análisis Fresnel
def fresnelAnalysis2(lnkDic, n, fPlot = False):#eVec, rVec
    #Configurando gráfica
    #CALCULOS
    path = pathCreator(lnkDic, n)
    eVec, rVec = getElevation(path)
    distVec = getDist(path)
    #Fresnel analysis variables
    b0 = eVec[0] + lnkDic['h1']
    h2 = eVec[-1] + lnkDic['h2']
    f = lnkDic['freq']
    deltaH = b0 - h2
    Dalt = distVec[-1]
    De = math.sqrt(Dalt**2 + deltaH**2)
    beta = math.atan(-deltaH/Dalt)
    #b = math.sqrt((De*constants.speed_of_light)/(4*f))
    b = 1/2 * math.sqrt(constants.speed_of_light*De/f)
    m = -deltaH/Dalt
    Xc = Dalt/2
    lEq = lambda xi: m*(xi) + b0
    veclEq = np.vectorize(lEq)
    Yc = lEq(Xc)
    #Yc = m*(Xc) + eVec[0] + lnkDic['h1']
    Cf = De/2
    a = math.sqrt(Cf**2 + b**2)
    ay = a * math.sin(beta)
    ax = a * math.cos(beta)
    #Calculo de puntos críticos
    yiVec = veclEq(distVec)
    diEq = np.vectorize(lambda xi: math.sqrt(xi**2 + (b0-lEq(xi))**2))
    hdiEq = np.vectorize(lambda di: math.sqrt((di*(De-di)*constants.speed_of_light)/(De*f)))        
    tdiVec = diEq(distVec)
    hdiVec = hdiEq(tdiVec)
    yhdiVec = hdiVec * math.cos(beta)
    restVec = -tdiVec + De
    downP = yiVec - yhdiVec
    upP = yiVec + yhdiVec
    
    hmx = np.max([b0,h2,np.max(eVec)])
    hmin = np.min([b0,h2,np.min(eVec)])
    hn = hmx-hmin
    
    yMins = [hmin - hn*0.05]*n
    cpVec = eVec.copy()
    cpVec[0] = b0
    cpVec[-1] = h2    
    #Obstrucción de la zona de Fresnel
    obVec = fresnelOVec(downP,upP,cpVec, yhdiVec)
    if fPlot:
        #Importando diseño
        #if ffFlag:
        plt1.style.use('../Python/Style/style1.mplstyle')
        #    ffFlag = False
        #PLOT
        #Reajustando a un máximo de 10 etiquetas en visualización
        arr = np.linspace(0,n-1,10, dtype = int)
        tarr = [distVec[i] for i in arr]
        #Torres
        torresD = [distVec[i] for i in [0,-1]]
        torresMin = [eVec[i] for i in [0,-1]]
        torresMax = [b0,h2]
        #Creando figura
        cplot = plt1.figure()
        ax = cplot.gca()
        #Tamaño de márgenes
        plt1.xlim(-De*0.09,Dalt*1.09)
        #plt.ylim(hmin - hn*0.05,hmx + hn *0.2)#
        #Inicio ploteo
        ax.plot(distVec,eVec, markersize = 5, color = fressC2_d)
        fresEllips = Ellipse(xy = (Xc,Yc), fill = False, width = 2*a, height = 2*b, angle = math.degrees(beta), color = fressC2_d)
        plt1.vlines(torresD,torresMin,torresMax, color = "gray")#
        ax.add_patch(fresEllips)
        plt1.vlines(distVec,yMins,eVec, color = "green")#fresmC
        #Creado anotaciones con valores de Característica Fresnel
        stp = De/n
        lEq2 = lambda xi: m*(xi) + b0*1.08
        ystp = np.max(yhdiVec)
        for count, i in enumerate(obVec):
            cx = distVec[count]# + stp*0.4
            cy = cpVec[count] + ystp*0.3
            #cy = eVec[count] * 1.001
            if count in arr:
                plt1.annotate(format(i,'.2f'),(cx,cy), ha='center', color = fressC1, fontsize = 10)
        #Ajustando tamaño de letra en eje x
        if De>2000:
            ax.tick_params(axis='x', which='major', labelsize=8)
        #Modficiando tamaño de eje vertical
        plt1.ylim(hmin - hn*0.05,ax.get_yticks()[-1])
        #Configuración final
        plt1.xticks(ticks = distVec)
        plt1.xticks(ticks = tarr)
        plt1.title("Línea vista")
        import os
        cwd = os.getcwd()
        plt1.savefig(os.path.join(cwd, 'Fresnel_Feature.jpg'), dpi = 300)
        #Configurando color de margen
        plt1.rcParams['figure.facecolor'] = 'FFFFFFFF'
        plt1.show()
        #return ax
    return obVec, distVec, eVec


#Función para Fresnel masivo
def fresnelAnalysis3(x,n,freq):#eVec, rVec
    lnkDic = {
        'lat1':x['latitude'],
        'lon1':x['longitude'],
        'h1':x['h'],
        'lat2':x['latitude_neighbor'],
        'lon2':x['longitude_neighbor'],
        'h2':x['h_neighbor'],
        'freq':freq
    }
    try:
        #Asignando desde fila
        eNames = [f'e{i}' for i in range(1,n+1)]
        eVec = x[eNames]
        #CALCULOS
        path = pathCreator(lnkDic, n)
        distVec = getDist(path)
        #Fresnel analysis variables
        b0 = eVec[0] + lnkDic['h1']
        h2 = eVec[-1] + lnkDic['h2']
        f = lnkDic['freq']
        deltaH = b0 - h2
        Dalt = distVec[-1]
        De = math.sqrt(Dalt**2 + deltaH**2)
        beta = math.atan(-deltaH/Dalt)
        #b = math.sqrt((De*constants.speed_of_light)/(4*f))
        b = 1/2 * math.sqrt(constants.speed_of_light*De/f)
        m = -deltaH/Dalt
        Xc = Dalt/2
        lEq = lambda xi: m*(xi) + b0
        veclEq = np.vectorize(lEq)
        Yc = lEq(Xc)
        #Yc = m*(Xc) + eVec[0] + lnkDic['h1']
        Cf = De/2
        a = math.sqrt(Cf**2 + b**2)
        ay = a * math.sin(beta)
        ax = a * math.cos(beta)
        #Calculo de puntos críticos
        yiVec = veclEq(distVec)
        diEq = np.vectorize(lambda xi: math.sqrt(xi**2 + (b0-lEq(xi))**2))
        hdiEq = np.vectorize(lambda di: math.sqrt((di*(De-di)*constants.speed_of_light)/(De*f)))        
        tdiVec = diEq(distVec)
        hdiVec = hdiEq(tdiVec)
        yhdiVec = hdiVec * math.cos(beta)
        restVec = -tdiVec + De
        downP = yiVec - yhdiVec
        upP = yiVec + yhdiVec
        
        hmx = np.max([b0,h2,np.max(eVec)])
        hmin = np.min([b0,h2,np.min(eVec)])
        hn = hmx-hmin
        
        yMins = [hmin - hn*0.05]*n
        cpVec = eVec.copy()
        cpVec[0] = b0
        cpVec[-1] = h2    
        #Obstrucción de la zona de Fresnel
        obVec = fresnelOVec(downP,upP,cpVec, yhdiVec)
        return obVec
    except:
        return [np.nan]*n

#Función para graficar dada una fila
def fresnel_graph_df(x,n,freq,color):
    lnkDic = {
        'lat1':x['latitude'],
        'lon1':x['longitude'],
        'h1':x['h'],
        'lat2':x['latitude_neighbor'],
        'lon2':x['longitude_neighbor'],
        'h2':x['h_neighbor'],
        'freq':freq
    }
    #Titulo
    title = x['serialNumber'] + '-' + x['serialNumber_neighbor']
    #Obteniendo obstrucciones
    fresnelNames = [f'f{i}' for i in range(1,21)]
    obVec = x[fresnelNames]
    #Asignando desde fila
    eNames = [f'e{i}' for i in range(1,21)]
    eVec = x[eNames]
    #CALCULOS
    path = pathCreator(lnkDic, n)
    distVec = getDist(path)
    #Fresnel analysis variables
    b0 = eVec[0] + lnkDic['h1']
    h2 = eVec[-1] + lnkDic['h2']
    f = lnkDic['freq']
    deltaH = b0 - h2
    Dalt = distVec[-1]
    De = math.sqrt(Dalt**2 + deltaH**2)
    beta = math.atan(-deltaH/Dalt)
    #b = math.sqrt((De*constants.speed_of_light)/(4*f))
    b = 1/2 * math.sqrt(constants.speed_of_light*De/f)
    m = -deltaH/Dalt
    Xc = Dalt/2
    lEq = lambda xi: m*(xi) + b0
    veclEq = np.vectorize(lEq)
    Yc = lEq(Xc)
    #Yc = m*(Xc) + eVec[0] + lnkDic['h1']
    Cf = De/2
    a = math.sqrt(Cf**2 + b**2)
    ay = a * math.sin(beta)
    ax = a * math.cos(beta)
    #Calculo de puntos críticos
    yiVec = veclEq(distVec)
    diEq = np.vectorize(lambda xi: math.sqrt(xi**2 + (b0-lEq(xi))**2))
    hdiEq = np.vectorize(lambda di: math.sqrt((di*(De-di)*constants.speed_of_light)/(De*f)))        
    tdiVec = diEq(distVec)
    hdiVec = hdiEq(tdiVec)
    yhdiVec = hdiVec * math.cos(beta)
    restVec = -tdiVec + De
    downP = yiVec - yhdiVec
    upP = yiVec + yhdiVec
    hmx = np.max([b0,h2,np.max(eVec)])
    hmin = np.min([b0,h2,np.min(eVec)])
    hn = hmx-hmin
    yMins = [hmin - hn*0.05]*n
    cpVec = eVec.copy()
    cpVec[0] = b0
    cpVec[-1] = h2  
    #PLOT
    #Reajustando a un máximo de 10 etiquetas en visualización
    arr = np.linspace(0,n-1,10, dtype = int)
    tarr = [distVec[i] for i in arr]
    #Torres
    torresD = [distVec[i] for i in [0,-1]]
    torresMin = [eVec[i] for i in [0,-1]]
    torresMax = [b0,h2]
    #Creando figura
    #plot = plt1.figure()
    fig, ax = plt.subplots()
    #ax = cplot.gca()
    #Tamaño de márgenes
    plt1.xlim(-De*0.09,Dalt*1.09)
    #plt.ylim(hmin - hn*0.05,hmx + hn *0.2)#
    #Inicio ploteo
    ax.plot(distVec,eVec, markersize = 5, color = fressC2_d)
    fresEllips = Ellipse(xy = (Xc,Yc), fill = False, width = 2*a, height = 2*b, angle = math.degrees(beta), color = fressC2_d)
    plt1.vlines(torresD,torresMin,torresMax, color = "gray")#
    ax.add_patch(fresEllips)
    plt1.vlines(distVec,yMins,eVec, color = color)#fresmC
    #Creado anotaciones con valores de Característica Fresnel
    stp = De/n
    lEq2 = lambda xi: m*(xi) + b0*1.08
    ystp = np.max(yhdiVec)
    for count, i in enumerate(obVec):
        cx = distVec[count]# + stp*0.4
        cy = cpVec[count] + ystp*0.3
        #cy = eVec[count] * 1.001
        if count in arr:
            plt1.annotate(format(i,'.2f'),(cx,cy), ha='center', color = fressC1, fontsize = 10)
    #Ajustando tamaño de letra en eje x
    if De>2000:
        ax.tick_params(axis='x', which='major', labelsize=8)
    #Modficiando tamaño de eje vertical
    plt1.ylim(hmin - hn*0.05,ax.get_yticks()[-1])
    #Configuración final
    plt1.xticks(ticks = distVec)
    plt1.xticks(ticks = tarr)
    plt1.title(title)
    plt1.rcParams['figure.facecolor'] = 'FFFFFFFF'



warnings.simplefilter(action='ignore', category=RuntimeWarning)

if __name__ == "__main__":
    #Lectura durante desarrollo
    """
    with open('teVec.json', 'r') as f:
        teVec = json.load(f)
        f.close()
        
    with open('trVec.json', 'r') as f:
        trVec = json.load(f)
        f.close()
    """
    
    #Enlace de prueba
    linkData = {
        'lat1' : 14.2776,
        'lon1' : -90.7902,
        'h1' : 5,
        'lat2' : 14.3149,
        'lon2' : -90.777,
        'h2' : 15,
        'freq' : 915000000,
        }
    fresnelAnalysis(linkData,10, fPlot = True)


    








