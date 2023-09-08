psql --username "$POSTGRES_USER" --dbname postgres --command "CREATE DATABASE workshop_assets;"
psql --username "$POSTGRES_USER" --dbname workshop_assets <<SQL
CREATE TABLE units_sold(
    date DATE NOT NULL PRIMARY KEY,
    value int NOT NULL
);
CREATE TABLE revenue(
    date DATE NOT NULL PRIMARY KEY,
    value NUMERIC(18,2) NOT NULL
);
CREATE TABLE average_sales_price(
    date DATE NOT NULL PRIMARY KEY,
    value NUMERIC(18,2) NOT NULL
);
SQL
