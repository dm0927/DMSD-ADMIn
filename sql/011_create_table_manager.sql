CREATE TABLE MANAGER(
            SSN int primary key,
            Salary float,
            foreign key (SSN) references EMPLOYEE(SSN),
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );