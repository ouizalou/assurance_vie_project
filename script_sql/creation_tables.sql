
use assurance_vie;
-- Création de la table clients

CREATE TABLE clients (
    client_id INT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    date_naissance DATE,
    revenu_annuel DECIMAL(10,2),
    email VARCHAR(150),
    telephone VARCHAR(50),
    adresse VARCHAR(255),
    ville VARCHAR(100),
    code_postal VARCHAR(20)
);


-- Création de la table produits

CREATE TABLE IF NOT EXISTS produits (
    produit_id INT PRIMARY KEY,
    nom_produit VARCHAR(100) NOT NULL,
    type_produit VARCHAR(50) NOT NULL,
    taux_interet_annuel DECIMAL(4,2) NOT NULL CHECK (taux_interet_annuel >= 0)
);

-- Création de la table intermediaires


CREATE TABLE intermediaires (
    intermediaire_id INT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    type_intermediaire ENUM('Courtier', 'Agent', 'Mandataire') NOT NULL
);

-- Création de la table contrats

CREATE TABLE contrats (
    contrat_id INT PRIMARY KEY,
    client_id INT NOT NULL,
    produit_id INT NOT NULL,
    intermediaire_id INT NOT NULL,
    date_signature DATE NOT NULL,
    date_cloture DATE NOT NULL,
    capital_initial DECIMAL(12, 2) NOT NULL,
    statut ENUM('actif', 'cloture') NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (produit_id) REFERENCES produits(produit_id),
    FOREIGN KEY (intermediaire_id) REFERENCES intermediaires(intermediaire_id)
);

-- Création de la table operations
CREATE TABLE operations (
    operation_id INT PRIMARY KEY,
    contrat_id INT NOT NULL,
    date_operation DATE NOT NULL,
    type_operation ENUM('Versement', 'Rachat', 'Avenant') NOT NULL,
    montant DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table valeurs_contrat

CREATE TABLE valeurs_contrat (
    valeur_id INT PRIMARY KEY,
    contrat_id INT NOT NULL,
    date_valeur DATE NOT NULL,
    valeur DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table beneficiaires

CREATE TABLE beneficiaires (
    beneficiaire_id INT PRIMARY KEY,
    contrat_id INT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    lien ENUM('Conjoint', 'Enfant', 'Parent', 'ami', 'Autre') NOT NULL,
    pourcentage DECIMAL(5, 2) CHECK (pourcentage >= 0 AND pourcentage <= 100),
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table sinistres

CREATE TABLE sinistres (
    sinistre_id INT PRIMARY KEY,
    contrat_id INT NOT NULL,
    date_sinistre DATE NOT NULL,
    type_sinistre ENUM('Décès', 'Invalidité', 'veresement', 'Maladie grave') NOT NULL,
    montant DECIMAL(12, 2) NOT NULL,
    description TEXT,
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table versements_programmes

CREATE TABLE versements_programmes (
    versement_id INT PRIMARY KEY AUTO_INCREMENT,
    contrat_id INT,
    montant DECIMAL(10,2),
    frequence ENUM('mensuel', 'trimestriel', 'annuel'),
    date_debut DATE,
    date_fin DATE,
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table documents_contrat

CREATE TABLE documents_contrat (
    document_id INT PRIMARY KEY AUTO_INCREMENT,
    contrat_id INT,
    type_document VARCHAR(50),
    date_ajout DATE,
    chemin_acces VARCHAR(255),
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table historique_statuts_contrat

CREATE TABLE historique_statuts_contrat (
    historique_id INT PRIMARY KEY AUTO_INCREMENT,
    contrat_id INT,
    statut VARCHAR(50),
    date_statut DATE,
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table utilisateurs_portail

CREATE TABLE utilisateurs_portail (
    utilisateur_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    email VARCHAR(100),
    mot_de_passe_hash VARCHAR(255),
    date_creation DATE,
    dernier_acces DATETIME,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

-- Création de la table alertes_contrat

CREATE TABLE alertes_contrat (
    alerte_id INT PRIMARY KEY AUTO_INCREMENT,
    contrat_id INT,
    type_alerte VARCHAR(100),
    message TEXT,
    date_alerte DATETIME,
    statut ENUM('nouvelle', 'lue', 'resolue'),
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table evenements_audit


CREATE TABLE evenements_audit (
    evenement_id INT PRIMARY KEY AUTO_INCREMENT,
    utilisateur_id INT,
    action VARCHAR(100),
    description TEXT,
    date_evenement DATETIME,
    ip_utilisateur VARCHAR(45),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs_portail(utilisateur_id)
);

-- Création de la table rendez_vous

CREATE TABLE rendez_vous (
    rdv_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    intermediaire_id INT,
    date_heure DATETIME,
    lieu VARCHAR(255),
    objet VARCHAR(255),
    compte_rendu VARCHAR(255),
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (intermediaire_id) REFERENCES intermediaires(intermediaire_id)
);

-- Création de la table notifications_clients

CREATE TABLE notifications_clients (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    contenu VARCHAR(255),
    date_envoi DATETIME,
    lu BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

-- Création de la table repartition_beneficiaires

CREATE TABLE repartition_beneficiaires (
    repartition_id INT PRIMARY KEY AUTO_INCREMENT,
    contrat_id INT NOT NULL,
    beneficiaire_id INT NOT NULL,
    pourcentage DECIMAL(5,2) NOT NULL CHECK (pourcentage >= 0 AND pourcentage <= 100),
    date_debut DATE,
    date_fin DATE,
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id),
    FOREIGN KEY (beneficiaire_id) REFERENCES beneficiaires(beneficiaire_id)
);

-- Création de la table reclamations_clients

CREATE TABLE reclamations_clients (
    reclamation_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT NOT NULL,
    contrat_id INT,
    objet VARCHAR(255),
    description VARCHAR(255),
    date_reclamation DATETIME,
    statut ENUM('ouverte', 'en cours', 'resolue', 'fermee') DEFAULT 'ouverte',
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);

-- Création de la table commissions_intermediaires

CREATE TABLE commissions_intermediaires (
    commission_id INT PRIMARY KEY AUTO_INCREMENT,
    intermediaire_id INT NOT NULL,
    contrat_id INT NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    date_versement DATE,
    statut ENUM('en attente', 'payée') DEFAULT 'en attente',
    FOREIGN KEY (intermediaire_id) REFERENCES intermediaires(intermediaire_id),
    FOREIGN KEY (contrat_id) REFERENCES contrats(contrat_id)
);


