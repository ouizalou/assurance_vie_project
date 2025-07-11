# data_analyst
data-analyst-work
# Base de données Assurance Vie
## Description
Cette base de données modélise les données essentielles liées aux contrats d’assurance vie. Elle comprend les informations sur les clients, les contrats, les bénéficiaires désignés, les événements liés aux contrats, ainsi que les intermédiaires impliqués.

## 🗂️ Tables principales

| Table                        | Description |
|----------------------------- |-------------|
| `clients`                    | Informations sur les assurés |
| `produits`                   | Types de produits d’assurance vie |
| `intermediaires`             | Canaux de souscription (agent, courtier…) |
| `contrats`                   | Souscriptions d’assurance vie |
| `operations`                 | Versements, rachats |
| `valeurs_contrat`            | Évolution des encours |
| `versements_programmes`      | Échéancier de versements |
| `sinistres`                  | Événements impactant les contrats |
| `documents_contrat`          | Documents liés aux contrats |
| `alertes_contrat`            | Notifications ou rappels |
| `historique_statuts_contrat` | Suivi des statuts dans le temps |
| `beneficiaires`              | Personnes désignées en cas de décès |
| `rendez_vous	`              |Rendez-vous entre clients et intermédiaires|
| `notifications_clients`      | Messages envoyés aux clients|
| `repartition_beneficiaires`  | Répartition des parts entre bénéficiaires|
| `reclamations_clients`       | Réclamations et demandes de support des clients|
| `commissions_intermediaires` | Commissions versées aux intermédiaires|


# 🖼️ Schéma relationnel (Mermaid) 

<img width="3840" height="562" alt="assurance_vie_mermaid" src="https://github.com/user-attachments/assets/e899d0fa-7075-465a-8ded-38eadc025661" />

