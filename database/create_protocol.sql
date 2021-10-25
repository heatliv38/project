CREATE TABLE `protocols` (
  `index` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `PMID` varchar(20) DEFAULT NULL,
  `date` varchar(30) DEFAULT NULL,
  `study_size` int DEFAULT NULL,
  `study_type` varchar(200) DEFAULT NULL,
  `analysis_type` varchar(200) DEFAULT NULL,
  `country` varchar(200) DEFAULT NULL,
  `DOI` varchar(200) DEFAULT NULL,
  `treatment_site` varchar(100) DEFAULT NULL,
  `T` varchar(10) DEFAULT NULL,
  `N` varchar(10) DEFAULT NULL,
  `M` varchar(10) DEFAULT NULL,
  `risk_group` varchar(100) DEFAULT NULL,
  `primary_site` varchar(100) DEFAULT NULL,
  `metastasis` varchar(10) DEFAULT NULL,
  `nodes_num` varchar(50) DEFAULT NULL,
  `staging_system` varchar(45) DEFAULT NULL,
  `histology` varchar(100) DEFAULT NULL,
  `margin` varchar(50) DEFAULT NULL,
  `PSA` varchar(30) DEFAULT NULL,
  `gleason` varchar(30) DEFAULT NULL,
  `recurrence` varchar(10) DEFAULT NULL,
  `volume_size` varchar(30) DEFAULT NULL,
  `dimension_size` varchar(30) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `clinical_risk` varchar(100) DEFAULT NULL,
  `performance_status` varchar(30) DEFAULT NULL,
  `age` varchar(30) DEFAULT NULL,
  `weight` varchar(30) DEFAULT NULL,
  `height` varchar(30) DEFAULT NULL,
  `gender_ratio` varchar(20) DEFAULT NULL,
  `race` varchar(100) DEFAULT NULL,
  `treatment_Intent` varchar(50) DEFAULT NULL,
  `retreat` varchar(20) DEFAULT NULL,
  `prior_RT` varchar(30) DEFAULT NULL,
  `surgery` varchar(50) DEFAULT NULL,
  `chemtherapy` varchar(30) DEFAULT NULL,
  `hormone` varchar(30) DEFAULT NULL,
  `immunotherapy` varchar(30) DEFAULT NULL,
  `ADT` varchar(100) DEFAULT NULL,
  `Regimen_I+` varchar(200) DEFAULT NULL,
  `RI_base_dose_fractions` varchar(45) DEFAULT NULL,
  `RI_boost_dose_modality` varchar(45) DEFAULT NULL,
  `RI_other_therapies` varchar(45) DEFAULT NULL,
  `RI_TCP_median_follow_up` varchar(45) DEFAULT NULL,
  `RI_local_control` varchar(45) DEFAULT NULL,
  `RI_overall_survival` varchar(45) DEFAULT NULL,
  `RI_PFS` varchar(45) DEFAULT NULL,
  `RI_bPFS` varchar(45) DEFAULT NULL,
  `RI_DFS` varchar(45) DEFAULT NULL,
  `RI_FFS` varchar(45) DEFAULT NULL,
  `RI_MFS` varchar(45) DEFAULT NULL,
  `RI_CSS` varchar(45) DEFAULT NULL,
  `RI_DMFS` varchar(45) DEFAULT NULL,
  `RI_BCR` varchar(45) DEFAULT NULL,
  `RI_NTCP_median_follow_up` varchar(45) DEFAULT NULL,
  `RI_toxicity_system` varchar(45) DEFAULT NULL,
  `RI_acute` varchar(100) DEFAULT NULL,
  `RI_G1+` varchar(100) DEFAULT NULL,
  `RI_G2+` varchar(100) DEFAULT NULL,
  `RI_G3+` varchar(100) DEFAULT NULL,
  `RI_G4+` varchar(100) DEFAULT NULL,
  `RI_G5` varchar(100) DEFAULT NULL,
  `Regimen_II+` varchar(200) DEFAULT NULL,
  `RII_base_dose_fractions` varchar(100) DEFAULT NULL,
  `RII_boost_dose_modality` varchar(45) DEFAULT NULL,
  `RII_other_therapies` varchar(45) DEFAULT NULL,
  `RII_TCP_median_follow_up` varchar(45) DEFAULT NULL,
  `RII_local_control` varchar(45) DEFAULT NULL,
  `RII_overall_survival` varchar(45) DEFAULT NULL,
  `RII_PFS` varchar(45) DEFAULT NULL,
  `RII_bPFS` varchar(45) DEFAULT NULL,
  `RII_DFS` varchar(45) DEFAULT NULL,
  `RII_FFS` varchar(45) DEFAULT NULL,
  `RII_MFS` varchar(45) DEFAULT NULL,
  `RII_CSS` varchar(45) DEFAULT NULL,
  `RII_DMFS` varchar(45) DEFAULT NULL,
  `RII_NTCP_median_follow_up` varchar(45) DEFAULT NULL,
  `RII_toxicity_system` varchar(45) DEFAULT NULL,
  `RII_acute` varchar(45) DEFAULT NULL,
  `RII_G1+` varchar(100) DEFAULT NULL,
  `RII_G2+` varchar(100) DEFAULT NULL,
  `RII_G3+` varchar(100) DEFAULT NULL,
  `RII_G4+` varchar(100) DEFAULT NULL,
  `RII_G5` varchar(100) DEFAULT NULL,
  `modality` varchar(45) DEFAULT NULL,
  `planning` varchar(45) DEFAULT NULL,
  `delivery` varchar(45) DEFAULT NULL,
  `imaging` varchar(45) DEFAULT NULL,
  `setup` varchar(45) DEFAULT NULL,
  `key_conclusion` varchar(500) DEFAULT NULL,
  `target_dose_constraints` varchar(45) DEFAULT NULL,
  `OAR_constraints` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;