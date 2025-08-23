# 📘 Projet Assurance Vie Risque

## 🎯 Objectif
Analyser et prédire les **montants investis par les clients** dans les contrats d’assurance vie afin de :  
- identifier les **clients VIP** (à fort potentiel),  
- suivre l’évolution des investissements,  
- mettre en place un **scoring automatisé** grâce au Machine Learning.  

---

## 📂 Données utilisées
Base **assurance_vie_risque** (MySQL) :  
- `clients_a` → informations client  
- `contrats` → contrats d’assurance vie  
- `operations` → transactions (versements, retraits, arbitrages)  
- `valeurs_contrat`, `produits`, `beneficiaires`, `versements_programmes`, `notifications_clients`, `sinistres`  

---

## 🛠️ Préparations & Analyses
- Nettoyage et normalisation des **clients, contrats et opérations**  
- Création d’agrégations :  
  - **montant investi par client et contrat**  
  - **rang investisseur**  
  - **segmentation VIP**  

---

## 📓 Notebooks
- **montant_investi_par_client** : calculs exploratoires et tests de transformations avant industrialisation.
- **montant_investi_model** : script d’entraînement ML + scoring VIP.
---

## 🤖 Machine Learning
### Modèles testés (Session 7 – 19/08/2025)
| Modèle              | R² (Test) |
|---------------------|-----------|
| 🌳 Decision Tree    | **0.999** |
| 🌲 Random Forest    | 0.996     |

**Variables les plus influentes** :  
1. `rang_investisseur`  
2. `nbre_contrat_investi`  
3. `client_id`  

📌 **Conclusion** : modèles très performants, avec un risque de sur-apprentissage pour le Decision Tree.  

---

## ⚙️ Automatisation
### Scénario : **SCORING_VIP_CLIENTS**
- Étapes exécutées :  
  1. Build **montant_investi**  
  2. Build **montant_investi_predic_model**  
  3. Build **top_clients_vip**  
- Exécution régulière (~20s)  
- Résultat : génération automatique d’un **scoring clients VIP** et mise à jour des indicateurs.  

---

## 📊 Dashboard : assurance_vie_clients_contrat
3 pages principales :  
1. **Classement clients** : montant investi, nombre de contrats, rang investisseur.  
2. **Analyse par nom** : moyenne des montants investis.  
3. **Prédictions & VIP** : résultats du modèle ML + top clients VIP.  

**Insights inclus** :  
- `montant_investi_par_client`  
- `moyennes par nom`  
- `prédictions des montants futurs`  
- `top clients VIP`  

---

## 🚀 Conclusion
Le projet fournit une **vue consolidée des investissements réels et prédits** en assurance vie.  
Il permet de :  
- cibler les **clients stratégiques**,  
- anticiper les comportements d’investissement,  
- automatiser la mise à jour des analyses et dashboards.  

