USE buisness;

INSERT INTO Cities (ID, Name, Region, Population, FoundationDate, Area)
VALUES
    (1, 'Минск', 'Минский', 1949070, 1067, 348),
    (2, 'Гомель', 'Гомельский', 501802, 1142, 139),
    (3, 'Брест', 'Брестский', 324461, 1019, 145);

INSERT INTO Organizations (ID, Name, LegalAddress, CityID, Rating)
VALUES
    (1, 'Брестмаш', 'г. Брест, ул. Суворова, 21В', 3, 3.4),
    (2, 'МТЗ', 'г. Минск, ул. Долгобродская, 29', 1, 4.3),
    (3, 'Гомельэнерго', 'г. Гомель, ул. Фрунзе, 9', 2, 4.4);