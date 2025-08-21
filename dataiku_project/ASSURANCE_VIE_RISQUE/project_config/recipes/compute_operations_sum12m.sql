SELECT 
    `contrat_id` AS `contrat_id`,
    SUM(`montant`) AS `montant_sum`,
    `type_operation`
  FROM (
    SELECT 
        `operation_id` AS `operation_id`,
        `contrat_id` AS `contrat_id`,
        `date_operation` AS `date_operation`,
        `type_operation` AS `type_operation`,
        `montant` AS `montant`
      FROM `ASSURANCE_VIE_RISQUE_operations_nettoyer`
    ) `dku__beforegrouping`
  GROUP BY `contrat_id`,`type_operation`