
# 📚 Imports externes
import streamlit as st
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
# bibliothèque standard qui fourni des outils pour travailler avec des flux Input/Output , flux en mémoire
import io
from sqlalchemy import create_engine

# 📁 Imports internes
from assurance_vie_analyse import (classement_client_par_montant_invest,
                                   valeur_moyenne_mensuelle_contrat,repartition_des_sinistres_par_produit
                                   ,nettoyer_donnees,nettoyer_donnees_clients,contrats__sinistre_produit,
                                   performance_produits,carte_noms_clients,capital_contrat_par_intermediaire,
                                   nbr_contrats_intermediaire)
host ='localhost'
port='3306'
DB_name='assurance_vie'
username='root'
password='root'

def get_engine():
    connection_string=f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{DB_name}'
    return create_engine(connection_string)

def load_sql(query,engine):
    try:
        df=pd.read_sql(query,engine)
        return df
    except Exception as e:
        print("❌ Erreur  de la requête sql :", e)
        return None

# Interface Streamlit
st.set_page_config(page_title="📊 Dashboard Assurance Vie",layout="wide")
st.title("🏛️ Dashboard d'Analyse - Assurance Vie")

# connexion a la base
engine=get_engine()

with st.spinner("⏳ Chargement des données..."):
    
    DF = load_sql("SELECT * FROM contrats", engine)
    DF_clients=load_sql("SELECT * FROM clients",engine)
    DF_produits=load_sql("SELECT * FROM produits",engine)
    DF_intermediaires=load_sql("SELECT * FROM intermediaires",engine)
    DF_sinistres=load_sql("SELECT * FROM sinistres",engine)
    DF_beneficiaires=load_sql("SELECT * FROM beneficiaires",engine)
    DF_operations=load_sql("SELECT * FROM operations",engine)
    DF_valeurs_contrat=load_sql("SELECT * FROM valeurs_contrat",engine)
    DF_versements_programmes=load_sql("SELECT * FROM versements_programmes",engine)
    DF_commissions_intermediaires=load_sql("SELECT * FROM commissions_intermediaires",engine)
    DF_repartition_beneficiaires=load_sql("SELECT * FROM repartition_beneficiaires",engine)

DF=nettoyer_donnees(DF)
DF_clients = nettoyer_donnees_clients(DF_clients)



col1, col2, col3, col4, col5= st.columns(5)
col1.metric("📄 Contrats", len(DF))
col2.metric("👥 Clients", len(DF_clients))
col3.metric("📄 Produits", len(DF_produits))
col4.metric("🛑 Contrats clôturés", DF[DF['statut'] == 'cloture'].shape[0])
col5.metric("✅ Contrats actifs", DF[DF['statut'] == 'actif'].shape[0])

# Ajouter un champ de saisie pour filtrer par client
Client=st.text_input("✍️ Entrez le nom du client","")
if Client:
    DF_clients["nom_complet"] = DF_clients["nom"] + " " + DF_clients["prenom"]
    resultat = DF_clients[DF_clients["nom_complet"].str.contains(Client, case=False, na=False)]
            
    if not resultat.empty :
        st.subheader(f" 🏆 Résultats pour le client : {Client}")
        st.dataframe(resultat[["client_id", "nom", "prenom", "date_naissance","revenu_annuel","adresse","ville", "code_postal"]])
        liste_ids = resultat["client_id"].tolist()
        query_inter = f"""
                        SELECT 
                        c.statut as statut_contrat,
                        i.intermediaire_id,
                        i.nom AS nom_intermediaire,
                        i.prenom AS prenom_intermediaire,
                        i.email,
                        i.telephone,
                        i.type_intermediaire,
                        COUNT(DISTINCT c.contrat_id) AS nb_contrats
                        FROM contrats c
                        JOIN intermediaires i ON c.intermediaire_id = i.intermediaire_id
                        JOIN clients cl ON c.client_id = cl.client_id
                        WHERE cl.client_id IN ({','.join(map(str, liste_ids))})
                        GROUP BY c.statut,i.intermediaire_id, i.nom, i.prenom, i.email, i.telephone, i.type_intermediaire
                        ORDER BY nb_contrats DESC
                         """
        df_inter = load_sql(query_inter, engine)
        if not df_inter.empty:
            st.subheader("📄 Intermédiaires associés :")
            filtered_dfN=df_inter[["nom_intermediaire","prenom_intermediaire","nb_contrats","statut_contrat"]]
            st.dataframe(filtered_dfN)

            intermediaire_choisi = st.selectbox("Choisissez un intermédiaire :", df_inter["nom_intermediaire"].unique())
            if intermediaire_choisi:
            # Filtrer et afficher uniquement pour cet intermédiaire
                filtered_df = df_inter[df_inter["nom_intermediaire"] == intermediaire_choisi][[
                "nom_intermediaire", "email", "telephone", "type_intermediaire",  "nb_contrats"
                 ]]
                st.dataframe(filtered_df)
        else:
            st.info("Aucun intermédiaire trouvé pour ce client.")
    else:
        st.warning("❌ Aucun client trouvé correspondant à ce nom.")




st.success("🧹✅ Données chargées et nettoyées !")

col1, col2, col3, col4, col5= st.columns(5)
col1.metric("📄 Bénéficiaires", len(DF_beneficiaires))
col2.metric("🏢 Intermédiares", len(DF_intermediaires))    
col3.metric("📈 valeurs de contrat", len(DF_valeurs_contrat))
col4.metric("⚠️ Sinistres", len(DF_sinistres))
col5.metric("💰 Operations", len(DF_operations))
with st.container():
    st.info("ℹ️ **Exploration des données** : utilisez le menu latéral pour afficher et filtrer les tables associées.")

option = st.sidebar.selectbox("🧐 Explorer les données :", ["Aucune", "Aperçu des tables"])

if option == "Aperçu des tables":
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "Clients", 
    "Produits", 
    "Intermédiaires", 
    "Sinistres", 
    "Bénéficiaires", 
    "Opérations", 
    "Valeurs de contrat", 
    "Versements programmés",
    "Répartition des bénéficiaires",
    "Commissions des intermédiaires"
])  
    with tab1:
        st.subheader("👥 Aperçu des clients")
        st.dataframe(DF_clients.sort_values(by="client_id",ascending=True).head(20))

    with tab2:
        st.subheader("📄 Aperçu des Produits ")
        st.dataframe(DF_produits.sort_values(by="produit_id",ascending=True).head(20))

    with tab3:
        st.subheader("🏢 Aperçu des Intermédiaires ")
        st.dataframe(DF_intermediaires.sort_values(by="intermediaire_id",ascending=True).head(20))

    with tab4:
        st.subheader("⚠️ Aperçu des Sinistres ")
        st.dataframe(DF_sinistres.sort_values(by="sinistre_id",ascending=True).head(20))

    with tab5:
        st.subheader("👥 Aperçu des benéfeciaires")
        st.dataframe(DF_beneficiaires.sort_values(by="beneficiaire_id",ascending=True).head(20))

    with tab6:
        st.subheader("💰 Aperçu des operations ")
        st.dataframe(DF_operations.sort_values(by="operation_id",ascending=True).head(20))

    with tab7:
        st.subheader("📈 Aperçu des valeurs de contrat ")
        st.dataframe(DF_valeurs_contrat.sort_values(by="valeur_id",ascending=True).head(20))

    with tab8:
        st.subheader("⏳ Aperçu des versements programmés ")
        st.dataframe(DF_versements_programmes.sort_values(by="versement_id",ascending=True).head(20))
    with tab9:
        st.subheader("📊 Répartition des bénéficiaires")
        st.dataframe(DF_repartition_beneficiaires.sort_values(by="repartition_id",ascending=True).head(20))
    with tab10:
        st.subheader("💼 Commissions des intermédiaires")
        st.dataframe(DF_commissions_intermediaires.sort_values(by="commission_id",ascending=True).head(20))


with st.container():
    st.info("📊 **Visualisations** – Utilisez le menu latéral pour afficher les graphiques.")


st.sidebar.markdown("## 🎯 Choisissez une visualisation")
visualisations = {
    "Aucune":"Aucune",
    "🏅 Classement des clients": "classement",
    "📉 Valeur mensuelle des contrats": "valeur_mensuelle",
    "🛡️ Répartition des sinistres": "sinistres",
    "📊 Performance des produits": "produits_perf",
    "📊 Performance des sinistres": "sinistres_perf"
}

choix_visu_label = st.sidebar.selectbox("📊 Visualisation :", list(visualisations.keys()))
choix_visu = visualisations[choix_visu_label]
if choix_visu == "classement":
    st.subheader("🏅 Classement des clients par investissement")
    st.info("15 meilleurs clients selon le montant total investi.")
    image_path = classement_client_par_montant_invest(engine)
    st.image(image_path, caption="🏅 Top investisseurs", use_container_width=True)

elif choix_visu == "valeur_mensuelle":
    st.subheader("📉 Valeur moyenne mensuelle des contrats")
    st.info("Évolution mensuelle moyenne des 100 contrats les plus investis.")
    image_path = valeur_moyenne_mensuelle_contrat(engine)
    st.image(image_path, caption="📉 Valeur moyenne mensuelle", use_container_width=True)

elif choix_visu == "sinistres":
    st.subheader("🛡️ Répartition des sinistres par produit")
    st.info("Visualisation de la fréquence des sinistres par type de produit.")
    image_path = repartition_des_sinistres_par_produit(engine)
    st.image(image_path, caption="🛡️ Sinistres par produit", use_container_width=True)

elif choix_visu == "sinistres_perf":
    st.subheader("📊 Visualisation interactive des sinistres")
    st.info("💬 Répartition des sinistres par type de produit et sinistre.")
    fig = contrats__sinistre_produit(engine, streamlit_mode=True)
    if fig:
        # st.plotly_chart(fig, use_container_width=True)
        st.success("✅ Graphique interactif affiché avec succès.")
elif choix_visu == "produits_perf":
    st.subheader("📊 Visualisation interactive des produits")
    st.info("💬 Performance des produits (capital moyen investi et nombre de contrats).")
    fig = performance_produits(engine, streamlit_mode=True)
    if fig:
        st.success("✅ Graphique interactif affiché avec succès.")

st.sidebar.header("🔎 Filtres des contrats")

statuts_disponibles = DF["statut"].unique().tolist()
statuts_selectionnes = st.sidebar.multiselect("📌 Sélectionnez un ou plusieurs statuts :", 
                                              options=statuts_disponibles,
                                              default=statuts_disponibles)

DF_filtre = DF[DF["statut"].isin(statuts_selectionnes)]
st.markdown(f"### 📄 Données filtrées ({len(DF_filtre)} contrats)")
st.dataframe(DF_filtre)

# Export Excel
excel_buffer = io.BytesIO()
DF_filtre.to_excel(excel_buffer, index=False, sheet_name="Contrats_Filtrés")
excel_buffer.seek(0)

# Bouton de téléchargement
if st.download_button(
    label="⬇️ Télécharger les données filtrées (.xlsx)",
    data=excel_buffer,
    file_name="contrats_filtres.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
):
    st.success("📁 Export Excel prêt au téléchargement !")


st.subheader("Analyse des intermédiaires")

filtre = st.selectbox(
    "Choisir l'affichage 👇",
    ["-", "Capital par intermédiaire", "Nombre de contrats"]
)

if filtre == "Capital par intermédiaire":
    capital_contrat_par_intermediaire(engine)

elif filtre == "Nombre de contrats":
    nbr_contrats_intermediaire(engine)



with st.expander("📍 Carte des clients (automatique via API)"):
    carte_noms_clients(engine)

