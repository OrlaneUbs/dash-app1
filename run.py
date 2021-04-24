# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 16:35:29 2021

@author: Orlane LE QUELLENNEC
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from flask import Flask
from plotly.subplots import make_subplots
import os

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

figMap = px.scatter_mapbox(us_cities.loc[[323], ['City', 'lat','lon',"State", "Population"]], lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
figMap.update_layout(mapbox_style="open-street-map")
figMap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#df = pd.read_csv('C:/Users/b-orl/OneDrive/Documents/Masters/Cours/S2/Optimisation/data/hour.csv')

df = pd.read_csv('hour.csv')

df.temp = df.temp*(39+8)-8
df.atemp = df.atemp*(50+16)-16

df["dteday"] = pd.to_datetime(df["dteday"], format="%Y-%m-%d")

df.sort_values("dteday", inplace=True)

aux2 = pd.DataFrame(columns=['dteday','cnt','registered','casual'])

k = 0;k1=0;k2=0; dte = df["dteday"][0]
for i in range(0,17379):
    if (df["dteday"][i] == dte):
        k = k + df["cnt"][i]
        k1 = k1 + df["registered"][i]
        k2 = k2 + df["casual"][i]
    if (df["dteday"][i] != dte):
        new_row = {'dteday':dte,'cnt':k,'registered':k1,'casual':k2}
        aux2 = aux2.append(new_row, ignore_index=True)
        k=0;k1=0;k2=0
        dte = df["dteday"][i]

#The application 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
'background': '#111111',
'text': '#7FDBFF'
}

app.layout = html.Div(
    children=[
        html.H1(children="Location de velos",),
        html.H2(children="Capital BikeShare Societe",),
        
        html.Div([
        html.H3('Velos'),
        html.P("3000")
    ]),
        
        html.Div([
        html.H3('Stations'),
        html.P("400")
    ]),
        
        html.Div([
        html.H3('Trajets/an'),
        html.P("2,1 millions")
    ]),
        
        html.P(
            children="Capital Bikeshare est un societe de location de velo en libre service. Initialement installee dans la ville Washington D.C. en 2010, elle est aujourd'hui un modele de reussite dans le secteur.",
        ),
        
        dcc.Graph(figure=figMap),
        
        html.H2(children="Le jeu de donnees",),
        html.P(
            children="On utilise le jeu de donnees 'Bike'. On affiche ce jeu de donnees ci-dessous.",
        ),
        
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in df.to_dict('records')
        ],
    
        # Overflow into ellipsis
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
         style_header={
             'textDecoration': 'underline',
             'textDecorationStyle': 'dotted',
        },
        page_size=15,
        data=df.to_dict('records')
        ),
    
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    
        html.H2(children="Evolution temporelle",),
        
        html.Div([
        html.H3('Nombre de location'),
        html.H4("3 292 679"),
        html.P("entre 2011 et 2012")
    ]),
        
        html.Div([
        html.H3('Progression des ventes'),
        html.H4("+ 37,75%"),
        html.P("entre 2011 et 2012")
    ]),

         html.P(
                    children="Analyse des locations de velos entre 2011 et 2012. L'utilisateur peut choisir le type d'utilisateur.",
                ),
        
        dcc.Dropdown(
        id="ticker",
        options=[{'label': 'Tous', 'value': 'cnt'},
        {'label': 'Abonnes', 'value': 'registered'},
        {'label': 'Non abonnes', 'value': 'casual'}],
        value='cnt',
    ),
        
        dcc.Graph(id="time-series-chart"),
        
        html.H2(children="Evolution meteorologique",),
        
        html.Div([
        html.H3('Temperature minimale'),
        html.P("-7,06")
    ]),
        
        html.Div([
        html.H3('Temperature maximal'),
        html.P("39")
    ]),

        
        dcc.Dropdown(
        id="tpc",
        options=[{'label': 'Tous', 'value': 'cnt'},
        {'label': 'Abonnes', 'value': 'registered'},
        {'label': 'Non abonnes', 'value': 'casual'}],
        value='cnt',
        clearable=False,
    ),
        
        dcc.RadioItems(
            id="tpm",
    options=[
        {'label': 'Temperature reelle', 'value': 'temp'},
        {'label': 'Temperature ressentie', 'value': 'atemp'},
        {'label': "Taux d'humidite", 'value': 'hum'},
        {'label': 'Force du vent', 'value': 'windspeed'}
    ],
    value='temp',
    labelStyle={'display': 'inline-block'}
    ),
        
        dcc.RadioItems(
            id="tps",
    options=[
        {'label': 'Saison', 'value': 'season'},
        {'label': 'Temps', 'value': 'weathersit'},
        {'label': "Jour travaille", 'value': 'workingday'}
    ],
    value='season',
    labelStyle={'display': 'inline-block'}
    ),
        dcc.Input(
            id="ttl",
            placeholder='Enter a title...',
            type='text',
            value=''
        )  ,
        
        dcc.Graph(id="meteo-chart"),
        
        
        html.H2(children="Prediction",),
        
        dcc.Tabs([
            dcc.Tab(label='Tous', children=[
                html.P("Le modele comprend 8 facteurs, la temperature ressentie, le taux d'humidite, la meteo, la saison, l'annee, l'heure, et le fait d'etre en vancances. On trouve une erreur quadratique de 70 625,18. Ce modele n'est pas tres performant, on conseille a la compagnie de ne pas considerer le modele lineaire pour predire le nombre totale de location a un instant t."),
    
            ]),
            dcc.Tab(label='Abonnes', children=[
                html.P("Le modele comprend 10 variables explicatives, la temperature ressentie, le taux d'humidite, la vitesse du vent, la meteo, le fait d'etre en week-end, la saison, l'heure, l'annee et le mois. On trouve une erreur quadratique de 53 903,83. Ce resultat est meilleur que le precedent mais reste decevant. On conseille a la compagnie de ne pas considerer le modele lineaire pour predire le nombre d'utilisation du service par les abonnes a un instant t."),
            ]),
            dcc.Tab(label='Non abonnes', children=[
                html.P("Le modele comprend 7 variables explicatives, la temperature ressentie, le taux d'humidite,le temps, la saison, l'annee, l'heure et le fait d'etre en vacances. On trouve une erreur quadratique de 1 400,137. Ce resultat est est convenable et bien meilleur que les precedents. On peut donc considerer le modele lineaire pour estimer le nombre de clients occasionnels a un instant t."),
            ]),
        ])
    ]
    
    
)

@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("ticker", "value")])
def display_time_series(ticker):
    fig = px.line(aux2, x='dteday', y=ticker)
    return fig

@app.callback(
    Output("meteo-chart", "figure"), 
    [Input("tpc","value"),Input("tpm","value"),Input("tps","value"),Input("ttl","value")])
def display_time_seriesbis(tpc,tpm,tps,ttl):
    fig = px.scatter(df, x=tpm, y=tpc, color=tps,title=ttl) 
    return fig


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "Bike.csv")


if __name__ == '__main__':
    app.run_server(debug=False)

