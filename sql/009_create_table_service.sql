CREATE TABLE SERVICE( 
            Service_ID int auto_increment, 
            Vehicle_type varchar(100), 
            Service_name varchar(100),
            Labor float, 
            Price float,
            Skill_ID int,
            primary key(Service_ID,Vehicle_type),
            foreign key (Skill_ID) references Skill(SKill_ID),
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );