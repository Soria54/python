#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: webToon
#------------------------------------------------------------

CREATE TABLE webToon(
        Id              Int  Auto_increment  NOT NULL ,
        nom             Varchar (255) NOT NULL ,
        moyenDateSortie Float
	,CONSTRAINT webToon_PK PRIMARY KEY (Id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: chapitre
#------------------------------------------------------------

CREATE TABLE chapitre(
        Id          Int  Auto_increment  NOT NULL ,
        numero      Int NOT NULL ,
        dateSortie  Datetime NOT NULL ,
        dateLecture Datetime ,
        site        Varchar (255) ,
        Id_webToon  Int NOT NULL
	,CONSTRAINT chapitre_PK PRIMARY KEY (Id)

	,CONSTRAINT chapitre_webToon_FK FOREIGN KEY (Id_webToon) REFERENCES webToon(Id)
)ENGINE=InnoDB;

