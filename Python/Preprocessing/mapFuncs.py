import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, widgets, Output
from IPython.display import display
from Private.constants import mapbox_access_token

#Función mapas para rondas discretos
def Rdiscrete_map(df,clrDic, clrCat, twgDic, mtitle):
    # Evitando multiples mapas
    # Contenedor de salida mapa
    out = Output()
    display(out)

    #Creando figura
    fig = go.Figure()

    #Configurando estilo y token
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='mapbox://styles/mapbox/streets-v11',  # Opciones de mapa en documentación de mapbox
        ),
        width=600,
        height=400,
        margin={'t': 30, 'b': 10, 'l': 10, 'r': 50}
    )

    #Función de actualización
    def update_map(**kwargs):  # fDate
        tflag = True
        for kfield in twgDic.keys():
            if tflag:
                filtered_df = df[df[kfield] == twgDic[kfield].value]
                tflag = False
            else:
                filtered_df = filtered_df[filtered_df[kfield] == twgDic[kfield].value]

        cRound = filtered_df["round"].unique()[0]
        tcolors = filtered_df[clrCat].map(clrDic).tolist()

        #Limpiando traza existente
        fig.data = []

        for cat in filtered_df[clrCat].unique():
            df_cat = filtered_df[filtered_df[clrCat] == cat]

            fig.add_trace(go.Scattermapbox(
                lat=df_cat['latitude'],
                lon=df_cat['longitude'],
                mode='markers',
                marker=dict(size=9, color=clrDic[cat]),
                text=df_cat["CollectorNm"],
                name=cat
            ))

        #Actualizando layout
        fig.update_layout(
            mapbox_center={'lat': filtered_df['latitude'].mean(), 'lon': filtered_df['longitude'].mean()},
            title=dict(text="{} - Ronda {}".format(mtitle, cRound), x=0.5),
            mapbox_zoom=7.5,
        )

        #Mostrando figura
        with out:
            out.clear_output(wait=True)
            display(fig)

    #Usar la interactividad con la función de actualización del mapa y los widgets.
    interact(update_map, **twgDic)





#Función mapas para rondas continuos
def Rcontinuous_map(df,clrDic, clrCat, twgDic, mtitle):
    # Evitando multiples mapas
    # Contenedor de salida mapa
    out = Output()
    display(out)

    #Creando figura
    fig = go.Figure()

    #Configurando estilo y token
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='mapbox://styles/mapbox/streets-v11',  # Opciones de mapa en documentación de mapbox
        ),
        width=600,
        height=400,
        margin={'t': 30, 'b': 10, 'l': 10, 'r': 50}
    )

    #Función de actualización
    def update_map(**kwargs):  # fDate
        tflag = True
        for kfield in twgDic.keys():
            if tflag:
                filtered_df = df[df[kfield] == twgDic[kfield].value]
                tflag = False
            else:
                filtered_df = filtered_df[filtered_df[kfield] == twgDic[kfield].value]

        cRound = filtered_df["round"].unique()[0]
        tcolors = filtered_df[clrCat].map(clrDic).tolist()

        #Limpiando traza existente
        fig.data = []

        for cat in filtered_df[clrCat].unique():
            df_cat = filtered_df[filtered_df[clrCat] == cat]

            fig.add_trace(go.Scattermapbox(
                lat=df_cat['latitude'],
                lon=df_cat['longitude'],
                mode='markers',
                marker=dict(size=9, color=clrDic[cat]),
                text=df_cat["CollectorNm"],
                name=cat
            ))

        #Actualizando layout
        fig.update_layout(
            mapbox_center={'lat': filtered_df['latitude'].mean(), 'lon': filtered_df['longitude'].mean()},
            title=dict(text="{} - Ronda {}".format(mtitle, cRound), x=0.5),
            mapbox_zoom=7.5,
        )

        #Mostrando figura
        with out:
            out.clear_output(wait=True)
            display(fig)

    #Usar la interactividad con la función de actualización del mapa y los widgets.
    interact(update_map, **twgDic)

#Función de mapas para múltiples DFs
def Rdiscrete_map2(dfDic, twgDic, mtitle):#,clrDic, clrCat, twgDic,
    # Evitando multiples mapas
    # Contenedor de salida mapa
    out = Output()
    display(out)
    #Creando figura
    fig = go.Figure()
    #Configurando estilo y token
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='mapbox://styles/mapbox/streets-v11',  # Opciones de mapa en documentación de mapbox
        ),
        width=600,
        height=400,
        margin={'t': 30, 'b': 10, 'l': 10, 'r': 50}
    )

    #Función de actualización
    def update_map(**kwargs):  # fDate
        fig.data = []
        #Recorriendo diccionario
        for key in dfDic.keys():
            #Asignando dfs
            df = dfDic[key][0]
            clrDic = dfDic[key][1]
            clrCat = dfDic[key][2]
            tflag = True
            for kfield in twgDic.keys():
                if tflag:
                    filtered_df = df[df[kfield] == twgDic[kfield].value]
                    cRound = filtered_df["round"].unique()[0]
                    tflag = False
                else:
                    filtered_df = filtered_df[filtered_df[kfield] == twgDic[kfield].value]
            if clrCat != None:
                for cat in filtered_df[clrCat].unique():
                    df_cat = filtered_df[filtered_df[clrCat] == cat]
                    fig.add_trace(go.Scattermapbox(
                        lat=df_cat['latitude'],
                        lon=df_cat['longitude'],
                        mode='markers',
                        marker=dict(size=9, color=clrDic[cat]),
                        text=df_cat[dfDic[key][3]],
                        name=cat
                    ))
                #Posiblemente requiera indentación
                #Actualizando layout
                fig.update_layout(
                    mapbox_center={'lat': filtered_df['latitude'].mean(), 'lon': filtered_df['longitude'].mean()},
                    title=dict(text="{} - Ronda {}".format(mtitle, cRound), x=0.5),
                    mapbox_zoom=7.5,
                )
            else:
                #cRound = filtered_df["round"].unique()[0]
                #fig.data = []
                #cRound = filtered_df["round"].unique()[0]
                fig.add_trace(go.Scattermapbox(
                    lat=filtered_df['latitude'],
                    lon=filtered_df['longitude'],
                    mode='markers',
                    marker=dict(size=9, color=clrDic),
                    text=filtered_df[dfDic[key][3]],#filtered_df["CollectorNm"],
                    name=key#"colec"
                ))
                #Posiblemente requiera indentación
                #Actualizando layout
                fig.update_layout(
                    mapbox_center={'lat': filtered_df['latitude'].mean(), 'lon': filtered_df['longitude'].mean()},
                    title=dict(text="{} - Ronda {}".format(mtitle, cRound), x=0.5),
                    mapbox_zoom=7.5,
                )
        #Mostrando figura
        with out:
            out.clear_output(wait=True)
            display(fig)
    #Usar la interactividad con la función de actualización del mapa y los widgets.
    interact(update_map, **twgDic)

#Versión 3 del mapa
#Función de mapas para múltiples DFs
def Rdiscrete_map3(dfDic, twgDic, mtitle):#,clrDic, clrCat, twgDic,
    # Evitando multiples mapas
    # Contenedor de salida mapa
    out = Output()
    display(out)
    #Creando figura
    fig = go.Figure()
    #Configurando estilo y token
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='mapbox://styles/mapbox/streets-v11',  # Opciones de mapa en documentación de mapbox
        ),
        width=600,
        height=400,
        margin={'t': 30, 'b': 10, 'l': 10, 'r': 50}
    )

    #Función de actualización
    def update_map(**kwargs):  # fDate
        fig.data = []
        #Recorriendo diccionario
        for key in dfDic.keys():
            #Asignando dfs
            df = dfDic[key][0]
            clrDic = dfDic[key][1]
            clrCat = dfDic[key][2]
            lt = dfDic[key][4][0]
            ln = dfDic[key][4][1]
            tflag = True
            for kfield in twgDic.keys():
                if tflag:
                    filtered_df = df[df[kfield] == twgDic[kfield].value]
                    cRound = filtered_df["round"].unique()[0]
                    tflag = False
                else:
                    filtered_df = filtered_df[filtered_df[kfield] == twgDic[kfield].value]
            if clrCat != None:
                for cat in filtered_df[clrCat].unique():
                    df_cat = filtered_df[filtered_df[clrCat] == cat]
                    fig.add_trace(go.Scattermapbox(
                        lat=df_cat[lt],
                        lon=df_cat[ln],
                        mode='markers',
                        marker=dict(size=9, color=clrDic[cat]),
                        text=df_cat[dfDic[key][3]],
                        name=cat
                    ))
                #Posiblemente requiera indentación
                #Actualizando layout
                fig.update_layout(
                    mapbox_center={'lat': filtered_df[lt].mean(), 'lon': filtered_df[ln].mean()},
                    title=dict(text="{} - Ronda {}".format(mtitle, cRound), x=0.5),
                    mapbox_zoom=7.5,
                )
            else:
                #cRound = filtered_df["round"].unique()[0]
                #fig.data = []
                #cRound = filtered_df["round"].unique()[0]
                fig.add_trace(go.Scattermapbox(
                    lat=filtered_df[lt],
                    lon=filtered_df[ln],
                    mode='markers',
                    marker=dict(size=9, color=clrDic),
                    text=filtered_df[dfDic[key][3]],#filtered_df["CollectorNm"],
                    name=key#"colec"
                ))
                #Posiblemente requiera indentación
                #Actualizando layout
                fig.update_layout(
                    mapbox_center={'lat': filtered_df[lt].mean(), 'lon': filtered_df[ln].mean()},
                    title=dict(text="{} - Ronda {}".format(mtitle, cRound), x=0.5),
                    mapbox_zoom=7.5,
                )
        #Mostrando figura
        with out:
            out.clear_output(wait=True)
            display(fig)
    #Usar la interactividad con la función de actualización del mapa y los widgets.
    interact(update_map, **twgDic)

