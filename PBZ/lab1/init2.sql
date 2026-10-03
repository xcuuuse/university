PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS spj;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS parts;
DROP TABLE IF EXISTS suppliers;


CREATE TABLE suppliers (
    supplier_id    TEXT    PRIMARY KEY,
    supplier_name  TEXT    NOT NULL,
    status         INTEGER NOT NULL,
    city           TEXT    NOT NULL
);

INSERT INTO suppliers (supplier_id, supplier_name, status, city) VALUES
('П1', 'Петров',   20, 'Москва'),
('П2', 'Синицин',  10, 'Таллинн'),
('П3', 'Федоров',  30, 'Таллинн'),
('П4', 'Чаянов',   20, 'Минск'),
('П5', 'Крюков',   30, 'Киев');


CREATE TABLE parts (
    part_id    TEXT    PRIMARY KEY,
    part_name  TEXT    NOT NULL,
    color      TEXT    NOT NULL,
    size       INTEGER NOT NULL,
    city       TEXT    NOT NULL
);

INSERT INTO parts (part_id, part_name, color, size, city) VALUES
('Д1', 'Болт',    'Красный', 12, 'Москва'),
('Д2', 'Гайка',   'Зеленая', 17, 'Минск'),
('Д3', 'Диск',    'Черный',  17, 'Вильнюс'),
('Д4', 'Диск',    'Черный',  14, 'Москва'),
('Д5', 'Корпус',  'Красный', 12, 'Минск'),
('Д6', 'Крышки',  'Красный', 19, 'Москва');


CREATE TABLE projects (
    project_id    TEXT PRIMARY KEY,
    project_name  TEXT NOT NULL,
    city          TEXT NOT NULL
);

INSERT INTO projects (project_id, project_name, city) VALUES
('ПР1', 'ИПР1', 'Минск'),
('ПР2', 'ИПР2', 'Таллинн'),
('ПР3', 'ИПР3', 'Псков'),
('ПР4', 'ИПР4', 'Псков'),
('ПР5', 'ИПР4', 'Москва'),
('ПР6', 'ИПР6', 'Саратов'),
('ПР7', 'ИПР7', 'Москва');


CREATE TABLE spj (
    supplier_id  TEXT    NOT NULL,
    part_id      TEXT    NOT NULL,
    project_id   TEXT    NOT NULL,
    qty          INTEGER NOT NULL,
    PRIMARY KEY (supplier_id, part_id, project_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    FOREIGN KEY (part_id)     REFERENCES parts(part_id)         ON DELETE CASCADE,
    FOREIGN KEY (project_id)  REFERENCES projects(project_id)   ON DELETE CASCADE
);

INSERT INTO spj (supplier_id, part_id, project_id, qty) VALUES
('П1', 'Д1', 'ПР1', 200),
('П1', 'Д1', 'ПР2', 700),
('П2', 'Д3', 'ПР1', 400),
('П2', 'Д2', 'ПР2', 200),
('П2', 'Д3', 'ПР3', 200),
('П2', 'Д3', 'ПР4', 500),
('П2', 'Д3', 'ПР5', 600),
('П2', 'Д3', 'ПР6', 400),
('П2', 'Д3', 'ПР7', 800),
('П2', 'Д5', 'ПР2', 100),
('П3', 'Д3', 'ПР1', 200),
('П3', 'Д4', 'ПР2', 500),
('П4', 'Д6', 'ПР3', 300),
('П4', 'Д6', 'ПР7', 300),
('П5', 'Д2', 'ПР2', 200),
('П5', 'Д2', 'ПР4', 100),
('П5', 'Д5', 'ПР5', 500),
('П5', 'Д5', 'ПР7', 100),
('П5', 'Д6', 'ПР2', 200),
('П5', 'Д1', 'ПР2', 100),
('П5', 'Д3', 'ПР4', 200),
('П5', 'Д4', 'ПР4', 800),
('П5', 'Д5', 'ПР4', 400),
('П5', 'Д6', 'ПР4', 500);