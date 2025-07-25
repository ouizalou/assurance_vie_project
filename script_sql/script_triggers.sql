use assurance_vie;

/*
 * Trigger : tr_insert_statut_contrat
 * But métier : Enregistrer automatiquement le statut initial d’un contrat
 *              dans la table historique dès sa création.
 * Usage : Assurer une traçabilité complète de la vie du contrat dès l’insertion.
 */

delimiter //

create trigger tr_insert_statut_contrat 
after insert on contrats
for each row
begin
	insert into historique_statuts_contrat(contrat_id,statut,date_statut)
	values(new.contrat_id,new.statut,now());
end //

/*
 * Trigger : tr_update_statut_contrat
 * But métier : Ajouter une nouvelle ligne dans l’historique des statuts 
 *              chaque fois que le statut d’un contrat change.
 * Usage : Permettre de suivre l’évolution de statut d’un contrat dans le temps.
 */

create trigger tr_update_statut_contrat
after update on contrats
for each row
begin
	if new.statut <> old.statut then
		insert into historique_statuts_contrat(contrat_id,statut,date_statut)
		values(new.contrat_id,new.statut,now());
	end if;
	
end
//
delimiter ;


/*
 * Trigger : tr_prevent_versement_if_resilier
 * But métier : Empêcher toute tentative de versement programmé 
 *              sur un contrat ayant été résilié.
 * Usage : Garantir la validité des opérations sur les contrats actifs uniquement.
 */

delimiter 
//
create trigger tr_prevent_versement_if_resilier
before insert on versements_programmes
for each row
begin
	declare contrat_statut varchar(50);
	
	select statut into contrat_statut from contrats 
	where contrat_id=new.contrat_id;
	if contrat_statut='resilie' then
		signal sqlstate '45000'
		set message_text='Impossible d’effectuer un versement sur un contrat résilié.';
	end if;
end
//
delimiter ;

/*
 * Trigger : tr_journaliser_suppression_sinistre
 * But métier : Enregistrer dans une table d’audit toute suppression
 *              d’un sinistre.
 * Usage : Assurer la traçabilité des suppressions de sinistres, notamment
 *         pour répondre aux exigences de conformité et d’audit.
 */



delimiter
//
create trigger tr_journaliser_suppression_sinistre 
before delete on sinistres 
for each row 
begin
	insert into evenements_audit (utilisateur_id,action,description,date_evenement,ip_utilisateur) 
	values(null,'suppression sinistre',
	concat('Sinistre ID ', OLD.sinistre_id, ' supprimé pour contrat ', OLD.contrat_id),
	now(),'localhost');
end
//
delimiter ;

/*
 * Trigger : tr_historique_insert_sinistre
 * But métier : Journaliser dans une table d’audit tout ajout de sinistre
 *              lié à un contrat d'assurance.
 * Usage : Permettre un suivi complet des ajouts de sinistres dans 
 *         une logique de traçabilité, de conformité et d'analyse.
 */

delimiter
//
create trigger tr_historique_insert_sinistre 
after insert on sinistres 
for each row 
begin
	insert into evenements_audit (utilisateur_id,action,description,date_evenement,ip_utilisateur) 
	values(null,'AJOUT_SINISTRE',
	concat('Ajout d''un sinistre de type ', NEW.type_sinistre, ' pour le  contrat ', NEW.contrat_id),
	now(),'localhost');

end
//
delimiter ;


/*
 * Trigger : tr_historique_insert_beneficiaire
 * But métier : Journaliser dans une table d’audit tout ajout de bénéficiaire
 *              à un contrat.
 * Usage : Permettre un suivi complet des ajouts de bénéficiaires dans 
 *         une logique de transparence et de sécurité juridique.
 */


delimiter
//
create trigger tr_historique_insert_beneficiaire 
after insert on beneficiaires 
for each row 
begin
	insert into evenements_audit (utilisateur_id,action,description,date_evenement,ip_utilisateur) 
	values(null,'AJOUT_BENEFICIAIRE',
	concat('Ajout de ', NEW.nom, ' au contrat ', NEW.contrat_id),
	now(),'localhost');

end
//
delimiter ;


