CREATE TABLE CUSTOMER (
            Cust_ID int primary key auto_increment, 
            Name varchar(25), 
            Address varchar(35),
            Password varchar(60), 
            Phone BIGINT unique, 
            Email varchar(100) unique, 
            Credit_Card LONG,
            Status varchar(25),
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );