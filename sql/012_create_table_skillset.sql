CREATE TABLE SKILLSET(
            Skill_ID int auto_increment, 
            SSN int, 
            primary key(Skill_ID,SSN),
            foreign key (Skill_ID) references SKILL(Skill_ID),
            foreign key (SSN) references EMPLOYEE(SSN),
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );