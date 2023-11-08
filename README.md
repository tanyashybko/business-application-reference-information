# business-application-reference-information

# Названия справочников:

1. Организации
2. Города

# Перечни колонок в справочнике "Организации":

- ID (целое число)
- Название (текст)
- Юридический адрес (текст)
- Город ID (целое число)

# Перечни колонок в справочнике "Города":

- ID (целое число)
- Название (текст)
- Регион (текст)
- Население (целое число)
- Дата основания (дата)

Справочник "Организации" зависит от справочника "Города" через колонку "Город ID". Все необходимые типы данных (текст, дата, числовые данные) присутствуют в обоих справочниках.