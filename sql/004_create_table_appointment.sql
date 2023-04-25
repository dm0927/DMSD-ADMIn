CREATE TABLE APPOINTMENT( 
        Appoint_ID int primary key auto_increment, 
        Date date, 
        Location_ID int,
        Customer_ID int, 
        Vehicle_ID varchar(30),
        foreign key (Location_ID) references Location(Location_ID) on update cascade,
        foreign key(Customer_ID) references Customer(Cust_ID) on update cascade, 
        foreign key(Vehicle_ID) references Vehicle(Vehicle_ID) on update cascade,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );