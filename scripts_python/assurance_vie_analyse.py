# assurance_vie_analyse.py

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import os
import requests
import time
import plotly.express as px

GRAPH_DIR = 'graphiques'
os.makedirs(GRAPH_DIR, exist_ok=True)

def load_sql(query, engine):
    """Exécute une requête SQL et retourne un DataFrame."""
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print("❌ Erreur lors de la requête SQL :", e)
        return None


# ------------------- Fonctions principales -------------------

def classement_client_par_montant_invest(engine):
    query = """
        SELECT
            c.client_id,
            c.nom, c.prenom,
            COUNT(DISTINCT ct.contrat_id) AS nbre_contrat_investi,
            SUM(vp.montant) AS total_investi,
            RANK() OVER (ORDER BY SUM(vp.montant) DESC) AS rang_investisseur
        FROM clients c 
        JOIN contrats ct ON ct.client_id=c.client_id
        JOIN versements_programmes vp ON vp.contrat_id=ct.contrat_id
        GROUP BY c.client_id, c.nom, c.prenom
    """
    df_clients = load_sql(query, engine)
    if df_clients is None or df_clients.empty:
        print("⚠️ Aucune donnée à afficher.")
        return None

    df_clients = df_clients.sort_values(by="total_investi", ascending=False).head(15)
    plt.figure(figsize=(8, 6))
    sn.barplot(data=df_clients, y='total_investi', x='nom', palette="Spectral")
    plt.title("Montant total investi par client")
    plt.xlabel("Clients")
    plt.ylabel("Montant (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph_path = os.path.join(GRAPH_DIR, "classement_clients.png")
    plt.savefig(graph_path)
    plt.close()
    return graph_path


def valeur_moyenne_mensuelle_contrat(engine):
    query = """
        SELECT
            vc.contrat_id,
            DATE_FORMAT(vc.date_valeur,'%M - %Y') as mois,
            AVG(vc.valeur) AS valeur_moyenne
        FROM valeurs_contrat vc
        GROUP BY vc.contrat_id, mois
        ORDER BY vc.contrat_id
    """
    df = load_sql(query, engine)
    if df is None or df.empty:
        print("⚠️ Aucune donnée à afficher.")
        return None

    df = df.sort_values(by="valeur_moyenne", ascending=False).head(100)
    plt.figure(figsize=(12, 6))
    sn.lineplot(data=df, x="mois", y="valeur_moyenne", marker="D", color="blue")
    plt.title("Valeur moyenne mensuelle d'un contrat")
    plt.xlabel("Mois")
    plt.ylabel("Valeur moyenne")
    plt.xticks(rotation=90)
    plt.tight_layout()
    graph_path = os.path.join(GRAPH_DIR, "valeur_moyenne_mensuelle.png")
    plt.savefig(graph_path)
    plt.close()
    return graph_path


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
    if df is None or df.empty:
        print("⚠️ Aucune donnée à afficher.")
        return None

    plt.figure(figsize=(10, 6))
    ax = sn.barplot(data=df, y='nom_produit', x='nombre_sinistres', palette="Spectral")
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', padding=2)
    plt.title("Répartition des sinistres par produit")
    plt.xlabel("Nombre de sinistres")
    plt.ylabel("Produit")
    plt.tight_layout()
    graph_path = os.path.join(GRAPH_DIR, "repartition_sinistres.png")
    plt.savefig(graph_path)
    plt.close()
    return graph_path


# ------------------- Fonctions utilitaires -------------------

def nettoyer_donnees(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df.drop_duplicates(subset="contrat_id", inplace=True)
    df.dropna(subset=["contrat_id", "client_id", "produit_id", "intermediaire_id","date_signature"], inplace=True)
    return df


def nettoyer_donnees_clients(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df.drop_duplicates(subset="client_id", inplace=True)
    df.dropna(subset=["client_id", "nom", "prenom", "date_naissance","revenu_annuel","adresse","ville","code_postal"], inplace=True)
    return df


# ------------------- Fonctions interactives -------------------

def contrats__sinistre_produit(engine, streamlit_mode=False):
    query = """
        SELECT
            c.contrat_id, p.nom_produit, c.statut, s.type_sinistre, s.montant
        FROM contrats c 
        JOIN sinistres s ON c.contrat_id = s.contrat_id
        JOIN produits p ON c.produit_id = p.produit_id
    """
    df = load_sql(query, engine)
    if df is None or df.empty:
        if streamlit_mode:
            import streamlit as st
            st.warning("⚠️ Aucune donnée de sinistres disponible.")
        return None

    fig = px.bar(df, x="nom_produit", y="montant", color="type_sinistre",
                 title="Montants des sinistres par produit")
    fig.update_layout(xaxis_tickangle=-45, barmode="stack", margin=dict(l=20,r=20,t=60,b=20))
    if streamlit_mode:
        import streamlit as st
        st.plotly_chart(fig, use_container_width=True)
    return fig
