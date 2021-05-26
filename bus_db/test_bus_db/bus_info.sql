--  Simple bus info database
--  project team : Mooyaho
--  2021 ESE. Mechanical information Engineering, University Of Seoul.
--  made by Oh Jeongkyu. (kyukk7@gmail.com)


DROP DATABASE IF EXISTS bus_info;
CREATE DATABASE IF NOT EXISTS bus_info;
USE bus_info;

SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

DROP TABLE IF EXISTS bus_info;

/*!50503 set default_storage_engine = InnoDB */;
/*!50503 select CONCAT('storage engine: ', @@default_storage_engine) as INFO */;

CREATE TABLE bus_info (
    list_no	INT             NOT NULL,
    bus_num	INT          	NOT NULL,
    bus_uid	INT		NOT NULL,
    stop_sig	INT		NOT NULL,
    fall_sig    INT             NOT NULL,
    input_date  DATE            NOT NULL,
    PRIMARY KEY (list_no)
);

flush /*!50503 binary */ logs;

SELECT 'LOADING bus_info' as 'INFO';
source load_bus_info.dump ;


-- source show_elapsed.sql ;
