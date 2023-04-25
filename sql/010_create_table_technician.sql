CREATE TABLE TECHNICIAN(
            SSN int primary key,
            Hourly_rate float,
            foreign key (SSN) references EMPLOYEE(SSN),
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );