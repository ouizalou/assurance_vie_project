import dataiku
import pandas as pd

# -----------------------------
# 1️⃣ Charger le dataset scoré
# -----------------------------
input_dataset = dataiku.Dataset("montant_investi_predic_model")
df = input_dataset.get_dataframe()

# -----------------------------
# 2️⃣ Trier par probabilité VIP
# -----------------------------
df_sorted = df.sort_values(by="proba_vip", ascending=False)

# -----------------------------
# 3️⃣ Sélectionner les top clients
#    (ici top 20%, modifiable)
# -----------------------------
top_percent = 0.20
n_top = int(len(df_sorted) * top_percent)
df_top = df_sorted.head(n_top)

# -----------------------------
# 4️⃣ Sauvegarde dans un dataset
# -----------------------------
df_out = df_top[['client_id', 'total_investi', 'categorie_pred', 'proba_vip']]

output_dataset = dataiku.Dataset("top_clients_vip")
output_dataset.write_with_schema(df_out)
