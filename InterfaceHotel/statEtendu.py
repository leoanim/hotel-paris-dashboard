import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import os

def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "static", filename)

def figure():
    df_total = pd.read_csv(get_file_path("stat_etendu.csv"), sep=";")
    fig = px.line(df_total, x="date", y="etendu", markers=True, color_discrete_sequence = [ "#82DAD0"])
    return fig

# Utiliser le chemin relatif pour le fichier CSV
df = pd.read_csv(get_file_path("test_carte.csv"), sep=";")

def etendu_mois(df):
    etendu=[]
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
        price = df_mois["prices"].max() - df_mois["prices"].min()
        mois.append(price)
        etendu.append(mois)
    df_etendu = pd.DataFrame(data=etendu, columns=['date', 'etendu'])
    df_etendu.to_csv(get_file_path("stat_etendu.csv"), index=False, sep=";")