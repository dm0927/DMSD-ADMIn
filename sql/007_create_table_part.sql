CREATE TABLE PART(
            Part_ID int primary key AUTO_INCREMENT,
            Name varchar(25),
            Price float,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );