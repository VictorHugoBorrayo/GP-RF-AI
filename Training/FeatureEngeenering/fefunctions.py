#Funciones para Feature Engeenering
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import tensorflow as tf
from random import sample

#Función para lectura de archivos
def getNames(dataPath, extension):
  fileNames = []
  for f in os.listdir(dataPath):
    name, ext = os.path.splitext(f)
    if ext == extension:
      fileNames.append(os.path.join(dataPath,f))
  return fileNames

#Obteniendo salto
def gettingJump(path):
    try:
        return int(path.split(',')[-2])
    except:
        return np.nan

#Función para visualización de mapa
def crear_mapa(datos, access_token, centro, zoom=10, titulo="Mapa", dinamic_fig = True):
    fig = go.Figure()

    for etiqueta, info in datos.items():
        if type(info['size']) == int:
            size = info['size']
        else:
            size = info['df'][info['size']]
        fig.add_trace(go.Scattermapbox(
            lat=info['df'][info['coords'][0]],
            lon=info['df'][info['coords'][1]],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=size,
                color=info['color'],
            ),
            text=info['df'][info['hover_field']],
            name=etiqueta
        ))

    fig.update_layout(
        mapbox=dict(
            accesstoken=access_token,
            style='mapbox://styles/mapbox/streets-v11',
            center={"lat": centro[0], "lon": centro[1]},
            zoom=zoom,
        ),
        margin={"r": 20, "t": 40, "l": 20, "b": 20},
        title=titulo,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    if dinamic_fig:
        fig.show()
    else:
        fig.show("png")


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

#Función para visualización de imagenes satelitales
def mostrar_imagenes_cluster(imagenes_cluster, numero_cluster, base_title = "Cluster de imágenes"):
    #Validando imagenes en muestra
    tempDf = pd.DataFrame(imagenes_cluster, columns = ["imgName","cluster"])
    tempDf = tempDf[tempDf["cluster"] == numero_cluster]
    imagenes_cluster = tempDf.values.tolist()
    if len(imagenes_cluster) > 4:
        imagenes_cluster = sample(imagenes_cluster, 4)

    plt.figure(figsize=(10, 10))

    for i, (image_name, _) in enumerate(imagenes_cluster[:4]):
        ax = plt.subplot(2, 2, i + 1)
        #Apuntando a directorio
        image_path = f"../../Data/DataMart/transformedImages/{image_name}"
        image = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, (99, 99))
        plt.imshow(image.numpy().astype("uint8"))
        plt.title(image_name)
        plt.axis("off")
    plt.suptitle(f"{base_title} {numero_cluster}")
    plt.show()















