SELECT 
    cl.client_id,
    cl.nom,
    cl.prenom,
    c.statut,
    COUNT(c.contrat_id) AS nbr_contrats
FROM clients_a cl
LEFT JOIN contrats c 
       ON cl.client_id = c.client_id

GROUP BY cl.client_id, cl.nom, cl.prenom,c.statut;
