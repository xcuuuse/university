SELECT * FROM teachers; --1

SELECT *
FROM student_groups
WHERE specialty = 'ЭВМ'; --2

SELECT DISTINCT teacher_id, classroom
FROM teaching_assignments
WHERE subject_id = '18П'; --3

SELECT DISTINCT teaching_assignments.subject_id, subjects.subject_name
FROM teaching_assignments
JOIN subjects ON teaching_assignments.subject_id = subjects.subject_id
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE teachers.last_name = 'Костин'; --4


SELECT DISTINCT group_id
FROM teaching_assignments
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE teachers.last_name = 'Фролов'; --5


SELECT *
FROM subjects
WHERE specialty = 'АСОИ'; --6

SELECT *
FROM teachers
WHERE specialty LIKE '%АСОИ%'; --7


SELECT DISTINCT teachers.last_name
FROM teaching_assignments
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE classroom = 210; --8

SELECT subjects.subject_name, student_groups.group_name
FROM teaching_assignments
JOIN subjects ON teaching_assignments.subject_id = subjects.subject_id
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE classroom BETWEEN 100 AND 200; --9

SELECT a.group_id, b.group_id
FROM student_groups AS a
JOIN student_groups AS b ON a.specialty = b.specialty
WHERE a.group_id < b.group_id; --10


SELECT SUM(student_count)
FROM student_groups
WHERE specialty = 'ЭВМ'; --11

SELECT DISTINCT teacher_id
FROM teaching_assignments
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE specialty = 'ЭВМ'; --12

SELECT subject_id
FROM teaching_assignments
GROUP BY subject_id
HAVING COUNT(DISTINCT group_id) = (SELECT COUNT(*) FROM student_groups); --13

SELECT DISTINCT teachers.last_name
FROM teaching_assignments
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE teaching_assignments.subject_id in (
    SELECT subject_id
    FROM teaching_assignments
    WHERE teacher_id IN (
        SELECT teacher_id
        FROM teaching_assignments
        WHERE subject_id = '14П'
    )
); --14


SELECT *
FROM subjects
WHERE subject_id NOT IN (
    SELECT subject_id
    FROM teaching_assignments
    WHERE teacher_id = '221Л'
); --15

SELECT *
FROM subjects
WHERE subject_id NOT IN (
    SELECT subjects.subject_id 
    FROM teaching_assignments
    JOIN subjects ON teaching_assignments.subject_id = subjects.subject_id
    JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
    WHERE group_name = 'М-6'
); --16


SELECT *
FROM teachers
WHERE post = 'Доцент' AND teacher_id IN (
    SELECT teacher_id
    FROM teaching_assignments
    WHERE group_id IN ('3Г', '8Г')
    GROUP BY teacher_id
    HAVING COUNT(DISTINCT group_id) = 2
); --17



SELECT subject_id, teaching_assignments.teacher_id, group_id
FROM teaching_assignments
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE teachers.department = 'ЭВМ' AND teachers.specialty LIKE '%АСОИ%'; --18


SELECT DISTINCT student_groups.group_id
FROM student_groups
JOIN teachers ON student_groups.specialty = teachers.specialty; --19


SELECT DISTINCT teaching_assignments.teacher_id
FROM teaching_assignments
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
JOIN subjects ON teaching_assignments.subject_id = subjects.subject_id
WHERE teachers.department = 'ЭВМ' AND subjects.specialty = student_groups.specialty; --20


SELECT DISTINCT student_groups.specialty
FROM teaching_assignments
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE teachers.department = 'АСУ'; --21



SELECT subject_id
FROM teaching_assignments
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE student_groups.group_name = 'АС-8'; --22




SELECT student_groups.group_id
FROM teaching_assignments
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE student_groups.group_id NOT IN (
    SELECT group_id
    FROM teaching_assignments
    WHERE subject_id IN (
        SELECT subject_id
        FROM teaching_assignments
        JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
        WHERE student_groups.group_name = 'АС-8'
    )
); --24

-- 1.23. Получить номера студенческих групп, которые изучают те же предметы, что и студенческая
--группа АС-8. ДОДЕЛАТЬ

SELECT DISTINCT group_id
FROM teaching_assignments
WHERE group_id NOT IN (
    SELECT group_id
    FROM teaching_assignments
    WHERE subject_id in (
        SELECT subject_id
        FROM teaching_assignments
        WHERE teacher_id = '430Л'
    )
); --25



SELECT teacher_id
FROM teaching_assignments
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE student_groups.group_name = 'Э-15' AND teacher_id NOT IN (
    SELECT teacher_id
    FROM teaching_assignments
    WHERE subject_id = '12П'
); --26