# Создание таблиц в базе данных buisness

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

# Заполнение таблиц

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

#Описание базы данных

+------------------+
|     Cities       |
+------------------+
| ID (Primary Key) |
| Name             |
| Region           |
| Population       |
| FoundationDate   |
| Area             |
+------------------+

+----------------------+
|    Organizations     |
+----------------------+
| ID (Primary Key)     |
| Name                 |
| LegalAddress         |
| CityID (Foreign Key) |
| Rating               |
+----------------------+
Таблица "Cities" содержит информацию о городах. У нее есть следующие столбцы:

ID: уникальный идентификатор города (первичный ключ).
Name: название города.
Region: регион, к которому относится город.
Population: население города.
FoundationDate: дата основания города.
Area: площадь города.
Таблица "Organizations" содержит информацию о различных организациях. У нее есть следующие столбцы:

ID: уникальный идентификатор организации (первичный ключ).
Name: название организации.
LegalAddress: юридический адрес организации.
CityID: идентификатор города, к которому относится организация (внешний ключ, связь с таблицей "Cities").
Rating: рейтинг организации.
Таблицы "Cities" и "Organizations" связаны между собой через столбец "CityID" в таблице "Organizations", который является внешним ключом, ссылается на столбец "ID" в таблице "Cities". Это позволяет связывать каждую организацию с соответствующим городом.
