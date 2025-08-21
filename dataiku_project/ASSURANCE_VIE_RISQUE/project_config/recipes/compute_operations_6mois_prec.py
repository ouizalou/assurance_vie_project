import dataiku
import pandas as pd

# === INPUT ===
# Dataset déjà agrégé sur 6 mois
df_6m = dataiku.Dataset("operation_sum6mois").get_dataframe()

# Si besoin, on peut renommer les colonnes ou faire un traitement simple
# Ici, juste pour l'exemple, on conserve les colonnes existantes
df_final = df_6m.copy()

# === OUTPUT ===
dataiku.Dataset("operations_6mois_prec").write_with_schema(df_final)
