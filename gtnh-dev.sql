create table if not exists logs ( id INT AUTO_INCREMENT PRIMARY KEY, time DATETIME, source_id INT, level INT NOT NULL, message TEXT );
create table if not exists client_ids ( id INT AUTO_INCREMENT PRIMARY KEY, cpu_uuid UUID );
create table if not exists client_hartbeat ( id INT PRIMARY KEY, time DATETIME );
create table if not exists client_metadata ( id INT PRIMARY KEY, first_seen DATETIME, location VARCHAR(128), description VARCHAR(1024) );
create table if not exists power_monitoring ( id INT AUTO_INCREMENT PRIMARY KEY, time DATETIME, source_id INT, consumption BIGINT );
create table if not exists item_ids ( id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(1024) );
create table if not exists item_stockpiles ( id INT AUTO_INCREMENT PRIMARY KEY, time DATETIME, client_ids INT, item_id INT, amount BIGINT UNSIGNED );