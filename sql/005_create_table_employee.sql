CREATE TABLE EMPLOYEE (
                SSN int primary key, 
                Name varchar(25), 
                email varchar(100) unique, 
                password varchar(60),
                Hire_date date,
                Role varchar(25), 
                Location_ID int,
                foreign key (Location_ID) references Location(Location_ID),
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );