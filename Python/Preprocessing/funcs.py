#

import os
import matplotlib.pyplot as plt
import pandas as pd



#Función para lectura de archivos
def getNames(dataPath, extension):
  fileNames = []
  for f in os.listdir(dataPath):
    name, ext = os.path.splitext(f)
    if ext == extension:
      fileNames.append(os.path.join(dataPath,f))
  return fileNames


#Concatenando archivos de carpeta data points
def createContainer(fList, ext):
    flag = True
    for i in fList:
        cName = i.split("\\")[-1]
        if ext == ".json":
            tdf = pd.read_json(i)
        elif ext == ".parquet":
            tdf = pd.read_parquet(i)
        elif ext == ".xlsx":
            tdf = pd.read_excel(i)
        else:
            pass
        tdf["fName"] = cName
        if flag:
            container = tdf
            flag = False
        else:
            container = pd.concat([container,tdf], ignore_index = True)
    return container



#Función genérica para detección de cambios en un DataFrame
def detect_changes(df, cKeys, iCols):
    #Ordenando df
    df = df.sort_values(cKeys)
    # Columna cambio
    df['Change'] = False
    # Iterando sobre grupos según cKeys
    for _, group in df.groupby(cKeys):
        #Calculando diferencias
        diff = group[iCols].shift() != group[iCols]
        #Asignando valor True a elementos con cambio
        df.loc[diff.any(axis=1).index, 'Change'] = diff.any(axis=1)
    tMap = {True: "Cambio", False: "NoCambio"}
    df["Change"] = df["Change"].map(tMap)
    return df

#Función de actualización de dfs
def updateDf(mainDf,secDf,keyCols = [], updateCols = None, ovrw = True):
    orderCols = mainDf.columns.tolist()
    if updateCols is None:
        tempList = orderCols.copy()
        for item in keyCols:
            tempList.remove(item)
        updateCols = tempList
        #updateCols = orderCols
    mainDf = mainDf.set_index(keyCols)
    secDf = secDf.set_index(keyCols)
    mainDf.update(secDf[updateCols], overwrite = ovrw)
    mainDf = mainDf.reset_index()
    mainDf = mainDf[orderCols]
    return mainDf


#Función para impresión de gráficos de texto
def dic2Img(diccionario, colores_titulo, colores_filas, tamano_titulo, tamano_filas, tamano_figura, color_fondo):
    #Creación de figura
    fig, axs = plt.subplots(1, len(diccionario), figsize=tamano_figura)
    #Estableciendo color de fondo
    fig.patch.set_facecolor(color_fondo)
    #Se itera sobre cada item en el diccionario y su color correspondiente
    for ax, ((llave, valores), color_titulo, colores_valor) in zip(axs, zip(diccionario.items(), colores_titulo, colores_filas)):
        #Determinando posición
        inicio = 1.0 - ((1.0 / (len(valores) + 1)) / 2)
        #Titulo
        ax.text(0.5, inicio, f'{llave}:', color=color_titulo, transform=ax.transAxes,\
                fontsize=tamano_titulo, ha='center', va='center')
        for i, (valor, color_valor) in enumerate(zip(valores, colores_valor)):
            #Imprimiendo texto en imagen
            ax.text(0.5, inicio - (i + 1) * (1.0 / (len(valores) + 1)), valor, color=\
                color_valor, transform=ax.transAxes, fontsize=tamano_filas, ha='center', va='center')
        #Desactivando ejes
        ax.axis('off')
    #Mostrando figura
    plt.tight_layout()
    plt.show()


#Función para detección de outliers
def identificar_outliers(serie, factor_iqr=1.5):
    #Calculando cuartiles
    Q1 = serie.quantile(0.25)
    Q3 = serie.quantile(0.75)
    #Calculando rango intercuantil
    IQR = Q3 - Q1
    #Identificando outliers
    es_outlier = (serie < (Q1 - factor_iqr * IQR)) | (serie > (Q3 + factor_iqr * IQR))
    return es_outlier

#Detect outliers
def outliers_detector(serie, factor_iqr=1.5):
    #Calculando cuartiles
    Q1 = serie.quantile(0.25)
    Q3 = serie.quantile(0.75)
    #Calculando rango intercuantil
    IQR = Q3 - Q1
    #Identificando outliers
    tOtlr = (serie < (Q1 - factor_iqr * IQR)) | (serie > (Q3 + factor_iqr * IQR))
    tOtlr = tOtlr.map({True: 'outlier', False: 'normal'})
    return tOtlr






















