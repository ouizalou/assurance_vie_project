import pandas as pd
import seaborn as sn
import datetime as dt
import matplotlib.pyplot as plt
import os
import requests
import geopandas as gpd
import time
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine


GRAPH_DIR='graphiques'      # dossier contenant les images .png nommées par numéro de contrat
os.makedirs(GRAPH_DIR,exist_ok=True)

host='localhost'
port='3306'
DB_name='assurance_vie'
username='root'
password='root'

connection_string=f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{DB_name}'

try:
    engine=create_engine(connection_string)
except Exception as e:
    print("❌ Erreur lors de la connexion  :", e)


query="SELECT * FROM contrats"
def load_sql(query,engine):
    try:
        DF=pd.read_sql(query,engine)
        print("requête sql executée avec succès")
        return DF
    except Exception as e:
        print( "❌ Erreur  de la requête sql :", e)
        print("requête executée",query)
        return None
DF=load_sql(query,engine)
if DF is not None:
    print(DF.head())
else:
    print("⚠️ données non chargées ")


print (" classement des cients par montant total invisti \n")
def classement_client_par_montant_invest(engine):
    query=("""
        SELECT
            c.client_id,
            c.nom,c.prenom,
            count( distinct ct.contrat_id)as nbre_contrat_investi,
            sum(vp.montant) as total_investi,
            rank() over (order by SUM(vp.montant) desc) as rang_investiseur
        FROM clients c 
        JOIN contrats ct on ct.client_id=c.client_id
        JOIN versements_programmes vp on vp.contrat_id=ct.contrat_id
        GROUP BY c.client_id, c.nom,c.prenom""")
    DF_clients=load_sql(query,engine)
    DF_clients = DF_clients.sort_values(by="total_investi", ascending=False).head(15)
    if DF_clients is not None and not DF_clients.empty:
        print(DF_clients.head())
        plt.figure(figsize=(8,6))
        sn.barplot(data=DF_clients, y='total_investi', x='nom', palette="Spectral")
        plt.title("Montant total investi par client")
        plt.xlabel("Clients")
        plt.ylabel("Montant (€)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        if not os.path.exists(GRAPH_DIR):
            os.makedirs(GRAPH_DIR)

        graph_path = os.path.join(GRAPH_DIR, "Répartition_des_montants_par_compagnie.png")
        plt.savefig(graph_path)
        plt.close()
        return graph_path
    else:
        print("⚠️ Aucune donnée à afficher.")
        return None

    
classement_client_par_montant_invest(engine)


print("\n 📆 Valeur moyenne mensuelle d'un contrat \n")
def valeur_moyenne_mensuelle_contrat(engine):
    query="""
        SELECT
            vc.contrat_id,
            DATE_FORMAT(vc.date_valeur,'%M - %Y') as mois,
            avg(vc.valeur) as valeur_moyenne
        FROM valeurs_contrat vc
        GROUP BY vc.contrat_id,mois
        ORDER BY vc.contrat_id"""
    DF_contrats=load_sql(query,engine)
    DF_contrats=DF_contrats.sort_values(by="valeur_moyenne",ascending=False).head(100)

    if DF_contrats is not None and not DF_contrats.empty:

        print(DF_contrats.head())
        plt.figure(figsize=(12,6))
        sn.lineplot(data=DF_contrats,x="mois", y="valeur_moyenne",marker="D",color="blue")
        plt.title("Valeur moyenne mensuelle d'un contrat")
        plt.xlabel("mois")
        plt.ylabel("valeur moyenne d'un contrat")
        plt.xticks(rotation=90)
        plt.tight_layout()
        if not os.path.exists(GRAPH_DIR):
            os.makedirs(GRAPH_DIR)
        graph_path = os.path.join(GRAPH_DIR, "Valeur_moyenne_mensuelle_d'un_contrat.png")
        plt.savefig(graph_path)
        plt.close()
        return graph_path
    else:
        print("⚠️ Aucune donnée à afficher.")
        return None
valeur_moyenne_mensuelle_contrat(engine)


print(" 📊 Répartition des sinistres par produit \n ")
def repartition_des_sinistres_par_produit(engine):
    query = """
        SELECT 
            p.nom_produit,
            COUNT(s.sinistre_id) AS nombre_sinistres,
            ROUND(AVG(s.montant), 2) AS montant_moyen
        FROM sinistres s
        JOIN contrats c ON c.contrat_id = s.contrat_id
        JOIN produits p ON p.produit_id = c.produit_id
        GROUP BY p.nom_produit
        ORDER BY nombre_sinistres DESC
    """
    df = load_sql(query, engine)

    if df is not None and not df.empty:
        print(df.head())
        plt.figure(figsize=(10,6))
        ax = sn.barplot(data=df, y='nom_produit', x='nombre_sinistres', palette="Spectral")

        # Ajout des étiquettes sur les barres
        for i in ax.containers:
            ax.bar_label(i, label_type='edge', padding=2)

        plt.title("📊 Répartition des sinistres par produit")
        plt.xlabel("Nombre de sinistres")
        plt.ylabel("Produit")
        plt.tight_layout()
        if not os.path.exists(GRAPH_DIR):
            os.makedirs(GRAPH_DIR)
        graph_path = os.path.join(GRAPH_DIR, "Valeur_moyenne_mensuelle_d'un_contrat.png")
        plt.savefig(graph_path)
        plt.close()
        return graph_path
    else:
        print("⚠️ Aucune donnée à afficher.")
        return None

    
repartition_des_sinistres_par_produit(engine)


def nettoyer_donnees(DF) :
    DF=DF.copy()
    DF.columns=DF.columns.str.strip()
    DF.drop_duplicates(subset="contrat_id",inplace=True)
    DF.dropna(subset=["contrat_id", "client_id", "produit_id", "intermediaire_id","date_signature"],inplace=True)
    print("🧹✅ Données chargées et nettoyées !")
    return DF
# appel de la fonction nettoyer_donnees
DF=nettoyer_donnees(DF)

query="SELECT * FROM clients"
DF_clients=load_sql(query,engine)
print(DF_clients.head())
def nettoyer_donnees_clients(DF_clients):
    DF_clients=DF_clients.copy()
    DF_clients.columns=DF_clients.columns.str.strip()
    DF_clients.drop_duplicates(subset="client_id",inplace=True)
    DF_clients.dropna(subset=["client_id", "nom", "prenom", "date_naissance","revenu_annuel","adresse","ville","code_postal"],inplace=True)
    print("🧹✅ Données chargées et nettoyées !")
    return DF_clients
DF_clients=nettoyer_donnees_clients(DF_clients)


# 📋 Liste des contrats ayant subi un sinistre, avec le type, montant et nom du produit associé
def contrats__sinistre_produit(engine,streamlit_mode=False):
    query="""SELECT
                c.contrat_id,p.nom_produit ,c.statut,s.type_sinistre,s.montant
            FROM contrats c 
            JOIN sinistres s on c.contrat_id =s.contrat_id
            JOIN produits p on c.produit_id=p.produit_id """
    DF_sinistres_prod=load_sql(query,engine)
    if DF_sinistres_prod is not None and  not DF_sinistres_prod.empty:
        print(DF_sinistres_prod.head())
        fig=px.bar(DF_sinistres_prod,
                    x="nom_produit",
                    y="montant",
                    color="type_sinistre",
                    title=" Les montants des sinistres par produit"
                    #points="all", 
                    #notched=True
                    )
        # la methode update_layout permet de personnaliser le graphique
        # xaxis_tickangle permet de pivoter les etiquettes de l'axe x
        fig.update_layout( 
              xaxis_tickangle=-45,
            barmode="stack",
            margin=dict(l=20, r=20, t=60, b=20))
        if streamlit_mode:
            st.plotly_chart(fig, use_container_width=True,key="sinistres_produit_chart")
        else:
            #fig.show()
            fig.write_html("plot_interactif_sinistre_par_produit.html")
            print("✅ Fichier HTML interactif sauvegardé.")
        return fig
    else :
        if streamlit_mode:
            st.warning("⚠️ Aucune donnée de sinistres disponible.")
        else:
            print("⚠️ Aucune donnée de sinistres disponible.")
        return None

print("")
def performance_produits(engine,streamlit_mode=False):
    query="""SELECT 
                p.produit_id,
                p.nom_produit,
                COUNT(c.contrat_id) AS nombre_contrats,
                ROUND(AVG(c.capital_initial), 2) AS capital_moyen_investi
            FROM produits p
            LEFT JOIN contrats c ON c.produit_id = p.produit_id
            GROUP BY p.produit_id, p.nom_produit
            ORDER BY capital_moyen_investi DESC"""
    DF_produits=load_sql(query,engine)
    if DF_produits is not None and not DF_produits.empty:
        print(DF_produits.head())
        fig = px.scatter(
        DF_produits,
        x="nombre_contrats",
        y="capital_moyen_investi",
        size="capital_moyen_investi",
        color="nom_produit",
        title="📈 Nombre de contrats vs Capital moyen investi",
        labels={
            "nombre_contrats": "Nombre de contrats",
            "capital_moyen_investi": "Capital moyen investi (€)"
        },
        hover_name="nom_produit"
        )
        fig.update_layout(
        margin=dict(l=60, r=60, t=90, b=50)
        )


        if streamlit_mode:
            st.plotly_chart(fig, use_container_width=True,key="performance_produit_chart")
        else:
            fig.show()
            fig.write_html("plot_interactif_performance_produit.html")
            print("✅ Fichier HTML interactif sauvegardé.")
        return fig
    else :
        if streamlit_mode:
            st.warning("⚠️ Aucune donnée de sinistres disponible.")
        else:
            print("⚠️ Aucune donnée de sinistres disponible.")
        return None

def get_lat_lon(ville, code_postal):
    try:
        # On fusionne ville + code postal dans la requête `q`
        q = f"{ville} {code_postal}"
        url = f"https://api-adresse.data.gouv.fr/search/?q={q}&limit=1"
        response = requests.get(url)
        data = response.json()
        if data['features']:
            coords = data['features'][0]['geometry']['coordinates']
            return coords[1], coords[0]  # lat, lon
        else:
            return None, None
    except Exception as e:
        print(f"Erreur API Adresse : {e}")
        return None, None

def carte_noms_clients(engine):
    # Requête SQL : récupère les clients et leur ville/code postal
    query = """
        SELECT 
            c.client_id,
            c.nom,
            c.prenom,
            c.ville,
            c.code_postal
        FROM contrats ct
        JOIN clients c ON ct.client_id = c.client_id
        GROUP BY c.client_id, c.nom, c.prenom, c.ville, c.code_postal
    """
    DF_clients = load_sql(query, engine)

    # Vérifie que le DataFrame contient des données
    if DF_clients is None or DF_clients.empty:
        st.warning("⚠️ Aucune donnée client disponible.")
        return

    # Crée un champ "nom complet"
    DF_clients["nom_complet"] = DF_clients["prenom"] + " " + DF_clients["nom"]

    # Regroupe les clients par ville/code postal, et concatène leurs noms
    df_grouped = DF_clients.groupby(['ville', 'code_postal']).agg(
        noms_clients=('nom_complet', lambda x: ', '.join(x)),
        #nb_clients=('client_id', 'count')
    ).reset_index()

    # Récupère les coordonnées GPS pour chaque ville
    latitudes = []
    longitudes = []
    for _, row in df_grouped.iterrows():
        lat, lon = get_lat_lon(row['ville'], row['code_postal'])
        latitudes.append(lat)
        longitudes.append(lon)
        time.sleep(0.1)  # éviter de surcharger l’API

    df_grouped['lat'] = latitudes
    df_grouped['lon'] = longitudes
    df_grouped["taille_point"] = 20  # Valeur fixe ou autre logique

    df_grouped = df_grouped.dropna(subset=['lat', 'lon'])

    if df_grouped.empty:
        st.error("❌ Aucune coordonnée GPS trouvée. Vérifiez les noms de villes ou codes postaux.")
        return

    # Carte interactive avec noms des clients au survol
    fig = px.scatter_mapbox(
        df_grouped,
        lat="lat",
        lon="lon",
        color="code_postal",
        size="taille_point",
        hover_name="noms_clients",  # <- ici on affiche les noms
        hover_data={"ville": True,"noms_clients":True},  # infos supplémentaires
        zoom=5,
        title="📍 Répartition géographique des clients avec noms"
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0, "t":40, "l":0, "b":0})
    st.plotly_chart(fig, use_container_width=True)

print("capital collecté et nombre de contrats par intermédiaire")
def nbr_contrats_intermediaire(engine,streamlit_mode=False):
    query="""SELECT 
                i.intermediaire_id,
                i.prenom as prenom_intermediaire,
                i.nom AS nom_intermediaire,
                COUNT(c.contrat_id) AS nb_contrats
            FROM contrats c
            JOIN intermediaires i ON c.intermediaire_id = i.intermediaire_id
            GROUP BY i.intermediaire_id, i.nom,i.prenom
            ORDER BY nb_contrats DESC"""
        # Lecture des données depuis la base
    DF_nbr_inter = load_sql(query, engine)
    
    # Si Streamlit est activé, afficher le graphique
    if  DF_nbr_inter is not None and not DF_nbr_inter.empty:
        st.write(DF_nbr_inter.sort_values(by="nb_contrats",ascending=False).head(15))
        fig = px.bar(
            DF_nbr_inter,
            x="prenom_intermediaire",
            y="nb_contrats",
            text="nb_contrats",  
            color="nom_intermediaire",
            labels={
                "nom_intermediaire": "Intermédiaire",
                "nb_contrats": "Nombre de contrat decrochés"
            },
            title="📄 Nombre de contrat  decrochés par intermédiaire"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_tickformat=",",
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    return DF_nbr_inter 
def capital_contrat_par_intermediaire(engine ,streamlit_mode=False):
    query="""SELECT 
                i.intermediaire_id,
                i.nom AS nom_intermediaire,
                i.prenom as prenom_interdiaire,
                
                SUM(c.capital_initial) AS capital_total
            FROM contrats c
            JOIN intermediaires i ON c.intermediaire_id = i.intermediaire_id
            GROUP BY i.intermediaire_id, i.nom, i.prenom
            ORDER BY capital_total DESC"""
    # Lecture des données depuis la base
    DF_inter = load_sql(query, engine)
    
    # Si Streamlit est activé, afficher le graphique
    if  DF_inter is not None and not DF_inter.empty:
        st.write(DF_inter.sort_values(by="capital_total",ascending=False).head(15))

        fig = px.bar(
            DF_inter,
            x="prenom_interdiaire",
            y="capital_total",
            text="capital_total",  
            color="nom_intermediaire",
            labels={
                "nom_intermediaire": "Intermédiaire",
                "capital_total": "Capital collecté (€)"
            },
            title="🏦 Capital total collecté par intermédiaire"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_tickformat=",",
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    return DF_inter 

   