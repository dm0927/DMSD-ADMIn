CREATE TABLE INVOICE(
        Invoice_ID int primary key,
        Amount float,
        Date_paid date,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );