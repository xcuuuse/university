-- Лабораторная работа № 1. Задание 1
-- Схема и данные для SQLite 3
-- Запуск:  sqlite3 lab1.db < init.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS teaching_assignments;
DROP TABLE IF EXISTS student_groups;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS teachers;


-- ТАБЛИЦА 1.1. ПРЕПОДАВАТЕЛЬ
CREATE TABLE teachers (
    teacher_id  TEXT    PRIMARY KEY,  -- ЛичныйНомер
    last_name   TEXT    NOT NULL,     -- Фамилия
    post        TEXT    NOT NULL,     -- Должность
    department  TEXT    NOT NULL,     -- Кафедра
    specialty   TEXT    NOT NULL,     -- Специальность
    home_phone  INTEGER NOT NULL      -- ТелефонДомашний
);

INSERT INTO teachers (teacher_id, last_name, post, department, specialty, home_phone) VALUES
('221Л', 'Фролов',  'Доцент',    'ЭВМ',       'АСОИ, ЭВМ',               487),
('222Л', 'Костин',  'Доцент',    'ЭВМ',       'ЭВМ',                     543),
('225Л', 'Бойко',   'Профессор', 'АСУ',       'АСОИ, ЭВМ',               112),
('430Л', 'Глазов',  'Ассистент', 'ТФ',        'СД',                      421),
('110Л', 'Петров',  'Ассистент', 'Экономики', 'Международная экономика', 324);


-- ТАБЛИЦА 1.2. ПРЕДМЕТ
CREATE TABLE subjects (
    subject_id    TEXT    PRIMARY KEY,  -- КодовыйНомерПредмета
    subject_name  TEXT    NOT NULL,     -- НазваниеПредмета
    hours_num     INTEGER NOT NULL,     -- КоличествоЧасов
    specialty     TEXT    NOT NULL,     -- Специальность
    semester      INTEGER NOT NULL      -- Семестр
);

INSERT INTO subjects (subject_id, subject_name, hours_num, specialty, semester) VALUES
('12П', 'Мини ЭВМ', 36, 'ЭВМ',      1),
('14П', 'ПЭВМ',     72, 'ЭВМ',      2),
('17П', 'СУБД ПК',  48, 'АСОИ',     4),
('18П', 'ВКСС',     52, 'АСОИ',     6),
('34П', 'Физика',   30, 'СД',       6),
('22П', 'Аудит',    24, 'Бухучета', 3);


-- ТАБЛИЦА 1.3. СТУДЕНЧЕСКАЯ_ГРУППА
CREATE TABLE student_groups (
    group_id           TEXT    PRIMARY KEY,  -- КодовыйНомерГруппы
    group_name         TEXT    NOT NULL,     -- НазваниеГруппы
    student_count      INTEGER NOT NULL,     -- КоличествоЧеловек
    specialty          TEXT    NOT NULL,     -- Специальность
    headman_last_name  TEXT    NOT NULL      -- ФамилияСтаросты
);

INSERT INTO student_groups (group_id, group_name, student_count, specialty, headman_last_name) VALUES
('8Г',  'Э-12', 18, 'ЭВМ',                     'Иванова'),
('7Г',  'Э-15', 22, 'ЭВМ',                     'Сеткин'),
('4Г',  'АС-9', 24, 'АСОИ',                    'Балабанов'),
('3Г',  'АС-8', 20, 'АСОИ',                    'Чижов'),
('17Г', 'С-14', 29, 'СД',                      'Амросов'),
('12Г', 'М-6',  16, 'Международная экономика', 'Трубин'),
('10Г', 'Б-4',  21, 'Бухучет',                 'Зязюткин');


-- ТАБЛИЦА 1.4. ПРЕПОДАВАТЕЛЬ_ПРЕПОДАЕТ_ПРЕДМЕТЫ_В_ГРУППАХ
CREATE TABLE teaching_assignments (
    group_id    TEXT    NOT NULL,  -- КодовыйНомерГруппы
    subject_id  TEXT    NOT NULL,  -- КодовыйНомерПредмета
    teacher_id  TEXT    NOT NULL,  -- ЛичныйНомер
    classroom   INTEGER NOT NULL,  -- НомерАудитории
    PRIMARY KEY (group_id, subject_id, teacher_id),
    FOREIGN KEY (group_id)   REFERENCES student_groups(group_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)     ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)     ON DELETE CASCADE
);

INSERT INTO teaching_assignments (group_id, subject_id, teacher_id, classroom) VALUES
('8Г',  '12П', '222Л', 112),
('8Г',  '14П', '221Л', 220),
('8Г',  '17П', '222Л', 112),
('7Г',  '14П', '221Л', 220),
('7Г',  '17П', '222Л', 241),
('7Г',  '18П', '225Л', 210),
('4Г',  '12П', '222Л', 112),
('4Г',  '18П', '225Л', 210),
('3Г',  '12П', '222Л', 112),
('3Г',  '17П', '221Л', 241),
('3Г',  '18П', '225Л', 210),
('17Г', '12П', '222Л', 112),
('17Г', '22П', '110Л', 220),
('17Г', '34П', '430Л', 118),
('12Г', '12П', '222Л', 112),
('12Г', '22П', '110Л', 210),
('10Г', '12П', '222Л', 210),
('10Г', '22П', '110Л', 210);