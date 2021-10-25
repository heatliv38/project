CREATE TABLE `patients` (
<<<<<<< HEAD:database/create_patient.sql
  `index` int(11) NOT NULL AUTO_INCREMENT,
=======
  `index` int NOT NULL AUTO_INCREMENT,
>>>>>>> 65965f030f321e2bbe97a2bbfaee777e84d060a1:database/create_patient.sql
  `name` varchar(50) DEFAULT NULL,
  `MRN` varchar(50) DEFAULT NULL,
  `DOB` varchar(50) DEFAULT NULL,
  `age` varchar(50) DEFAULT NULL,
  `weight` varchar(50) DEFAULT NULL,
  `height` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `race` varchar(50) DEFAULT NULL,
  `performance_status` varchar(50) DEFAULT NULL,
  `treatment_site` varchar(50) DEFAULT NULL,
  `T` varchar(50) DEFAULT NULL,
  `N` varchar(50) DEFAULT NULL,
  `M` varchar(50) DEFAULT NULL,
  `risk_group` varchar(50) DEFAULT NULL,
  `primary_site` varchar(50) DEFAULT NULL,
  `metastasis` varchar(50) DEFAULT NULL,
  `nodes_num` varchar(50) DEFAULT NULL,
  `staging_system` varchar(50) DEFAULT NULL,
  `histology` varchar(50) DEFAULT NULL,
  `margin` varchar(50) DEFAULT NULL,
  `PSA` varchar(50) DEFAULT NULL,
  `gleason` varchar(50) DEFAULT NULL,
  `recurrence` varchar(50) DEFAULT NULL,
  `volume_size` varchar(50) DEFAULT NULL,
  `dimension_size` varchar(50) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `clinical_risk` varchar(50) DEFAULT NULL,
  `treatment_intent` varchar(50) DEFAULT NULL,
  `retreat` varchar(50) DEFAULT NULL,
  `prior_RT` varchar(50) DEFAULT NULL,
  `surgery` varchar(50) DEFAULT NULL,
  `chemtherapy` varchar(50) DEFAULT NULL,
  `hormone` varchar(50) DEFAULT NULL,
  `immunotherapy` varchar(50) DEFAULT NULL,
  `ADT` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`index`)
<<<<<<< HEAD:database/create_patient.sql
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
SELECT * FROM capstone.patients;
=======
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
>>>>>>> 65965f030f321e2bbe97a2bbfaee777e84d060a1:database/create_patient.sql
