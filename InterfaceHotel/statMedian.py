import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import os

def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "static", filename)

def figure():
    df_total = pd.read_csv(get_file_path("stat_median.csv"), sep=";")
    fig = px.line(df_total, x="date", y="median", markers=True, color_discrete_sequence = [ "#82DAD0"])
    return fig

# Utiliser le chemin relatif pour le fichier CSV
df = pd.read_csv(get_file_path("test_carte.csv"), sep=";")

def median_mois(df):
    median=[]
    indexNames = df[df['prices'] <= 20].index
    df.drop(indexNames, inplace=True)
    list_mois = df['start_date'].unique()
    for i in range(len(list_mois)):
        list_mois[i] = datetime.datetime.strptime(list_mois[i], "%m-%d-%Y")
    list_mois = sorted(list_mois)
    for i in range(len(list_mois)):
        list_mois[i] = datetime.datetime.strftime(list_mois[i], "%m-%d-%Y")
    for i in list_mois:
        mois=[]
        df = df[['start_date','prices']]
        df_mois = df[(df['start_date']== i)]
        mois.append(i)
        price = df_mois["prices"].median()
        mois.append(price)
        median.append(mois)
    df_median = pd.DataFrame(data=median, columns=['date', 'median'])
    df_median.to_csv(get_file_path("stat_median.csv"), index=False, sep=";")