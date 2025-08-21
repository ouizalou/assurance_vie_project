import dataiku
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# -----------------------------
# 1️⃣ Charger le dataset
# -----------------------------
df = dataiku.Dataset("montant_investi").get_dataframe()

# -----------------------------
# 2️⃣ Créer la colonne cible
# -----------------------------
seuil_vip = df['total_investi'].quantile(0.75)
df['categorie'] = df['total_investi'].apply(lambda x: 'VIP' if x > seuil_vip else 'Normal')

# -----------------------------
# 3️⃣ Définir les features
# -----------------------------
features = ['nbre_contrat_investi', 'rang_investisseur']
df = df.dropna(subset=features + ['categorie'])

X = df[features]
y = df['categorie']

# -----------------------------
# 4️⃣ Pipeline préprocessing + modèle
# -----------------------------
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    ))
])

# -----------------------------
# 5️⃣ Validation croisée + test
# -----------------------------
scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print("Accuracy moyenne (CV):", scores.mean())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))
print("\nRapport de classification :")
print(classification_report(y_test, y_pred))
print("AUC ROC:", roc_auc_score((y_test=="VIP").astype(int), y_proba))

# -----------------------------
# 6️⃣ Ajouter les prédictions
# -----------------------------
df['categorie_pred'] = pipeline.predict(X)
df['proba_vip'] = pipeline.predict_proba(X)[:, 1]

# -----------------------------
# 7️⃣ Sauvegarde dataset final
# -----------------------------
df_out = df[['client_id', 'nbre_contrat_investi', 'rang_investisseur', 
             'total_investi', 'categorie', 'categorie_pred', 'proba_vip']]

output_dataset = dataiku.Dataset("montant_investi_predic_model")
output_dataset.write_with_schema(df_out)
