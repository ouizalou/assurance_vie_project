# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
clients_a = dataiku.Dataset("clients_a")
clients_a_df = clients_a.get_dataframe()
contrats = dataiku.Dataset("contrats")
contrats_df = contrats.get_dataframe()
versements_programmes = dataiku.Dataset("versements_programmes")
versements_programmes_df = versements_programmes.get_dataframe()

# Jointures
df = contrats_df.merge(clients_a_df, on="client_id", how="inner")
df = df.merge(versements_programmes_df, on="contrat_id", how="inner")

# Agrégation : nombre de contrats distincts, total investi
agg_df = df.groupby(["client_id", "nom", "prenom"]).agg(
    nbre_contrat_investi=("contrat_id", "nunique"),
    total_investi=("montant", "sum")
).reset_index()

# Classement par montant investi
agg_df["rang_investisseur"] = agg_df["total_investi"].rank(method="dense", ascending=False).astype(int)

# Write recipe outputs
montant_investi = dataiku.Dataset("montant_investi")
montant_investi.write_with_schema(agg_df)
