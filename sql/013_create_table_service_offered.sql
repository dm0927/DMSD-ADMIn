CREATE TABLE SERVICE_OFFERED (
                Service_ID int auto_increment, 
                Vehicle_type varchar(25), 
                Part_id int, 
                primary key (Service_ID,Vehicle_type,Part_id), 
                foreign key (Service_ID,Vehicle_type) references Service(Service_ID,Vehicle_type),
                foreign key (Part_id) references PART(Part_ID),
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );