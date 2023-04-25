CREATE TABLE VEHICLE( 
        Vehicle_ID VARCHAR(30) primary key, 
        Year int, 
        Type varchar(25),
        Mfg varchar(25), 
        Model varchar(25),
        Color varchar(25), 
        Customer_ID int, constraint fk foreign key (Customer_ID) references CUSTOMER(Cust_ID) On update cascade,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ); 