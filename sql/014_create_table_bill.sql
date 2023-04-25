CREATE TABLE BILL(
            Appoint_ID int, 
            Vehicle_type varchar(25), 
            Service_ID int, 
            Invoice_ID int,
            Price float,
            primary key(Appoint_ID,Vehicle_type,Service_ID,Invoice_ID), 
            foreign key (Appoint_ID) references Appointment(Appoint_ID),
            foreign key (Service_ID,Vehicle_type) references Service(Service_ID,Vehicle_type),
            foreign key (Invoice_ID) references Invoice(Invoice_ID),
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );