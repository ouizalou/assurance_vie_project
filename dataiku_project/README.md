# 📊 Projet Dataiku – Assurance Vie

## 🚀 Contexte
Ce projet illustre l’utilisation de **Dataiku DSS** pour analyser une base de données d’assurance vie.  
Il reprend les mêmes données que celles définies dans le dossier `script_sql/` et les exploite dans un **workflow Dataiku** combinant :

- Importation des données (SQL / CSV générés).
- Nettoyage et préparation (recipes visuelles et scripts Python/SQL).
- Analyses exploratoires et indicateurs métiers.
- Modélisation prédictive simple.
- Dashboard interactif.

---

## 📂 Contenu du dossier
- `assurance_vie_dataiku.zip` → Export complet du projet Dataiku DSS.
- `screenshots/` → Captures d’écran du Flow, des dashboards et des analyses.
- `README.md` → Documentation du projet.

---

## 🛠️ Prérequis
- **Dataiku DSS** (≥ version 11, Community Edition gratuite suffit).  
  👉 [Téléchargement Dataiku DSS](https://www.dataiku.com/product/get-started/)  
- Base de données  `script_sql/`.

---

## 📥 Importer le projet
1. Ouvrir **Dataiku DSS**.
2. Aller dans **Projects > Import project**.
3. Sélectionner le fichier `assurance_vie_dataiku.zip`.
4. Le projet apparaît dans vos projets DSS avec le Flow complet.

---

## 📊 Exemple de Flow
![Flow Screenshot](screenshots/flow.png)

- **Données sources** : contrats, opérations, sinistres, bénéficiaires.  
- **Recipes** :
  - Nettoyage et jointures.
  - Agrégations (KPI : encours total, taux de sinistralité).
- **Analyses** :
  - Segmentation clients.
  - Prédiction simple de la résiliation (churn).

---

## 📈 Indicateurs métiers inclus
- Nombre total de contrats actifs / clôturés.
- Montant des rachats partiels et totaux.
- Répartition des bénéficiaires par type.
- Taux de sinistralité global.
- KPI financiers (encours total, commissions).

---

## 🤖 Modélisation
Un exemple de **modèle prédictif** est inclus (AutoML Dataiku) :
- Objectif : prédire la probabilité de résiliation d’un contrat.
- Algorithmes testés : régression logistique, random forest.
- Variables : âge assuré, ancienneté contrat, encours, nombre d’opérations.

---

## 📊 Dashboard
Un **dashboard Dataiku** est disponible :
- Graphiques interactifs (contrats, encours, sinistres).
- Filtres par période et type de produit.
- Visualisation du churn prédictif.

![Dashboard Screenshot](screenshots/dashboard.png)

---

## 🔄 Automatisation
Un scénario d’automatisation est configuré :
- Mise à jour quotidienne des données.
- Recalcul automatique des KPI et dashboards.
- Notifications par email (optionnel).

---

## ✅ Étapes futures
- Ajouter plus d’analyses prédictives (fraude, scoring clients).  
- Créer un pipeline automatisé avec export vers **Power BI** ou **Streamlit**.  
- Intégrer l’API Python de Dataiku pour lancer des scripts avancés.

---
