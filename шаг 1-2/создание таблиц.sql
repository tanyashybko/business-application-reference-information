USE buisness;
CREATE TABLE Cities (
    ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Region VARCHAR(255),
    Population INT,
    FoundationDate DATE,
    Area DECIMAL(10, 2)
);

CREATE TABLE Organizations (
    ID INT PRIMARY KEY,
    Name VARCHAR(255),
    LegalAddress VARCHAR(255),
    CityID INT,
    Rating DECIMAL(10, 2),
    FOREIGN KEY (CityID) REFERENCES Cities(ID)
);