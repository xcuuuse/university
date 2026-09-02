SELECT * FROM teachers; --1

SELECT *
FROM student_groups
WHERE specialty = 'ЭВМ'; --2

SELECT DISTINCT teacher_id, classroom
FROM teaching_assignments
WHERE subject_id = '18П' --3

SELECT DISTINCT teaching_assignments.subject_id, subjects.subject_name
FROM teaching_assignments
JOIN subjects ON teaching_assignments.subject_id = subjects.subject_id
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE teachers.last_name = 'Костин' --4


SELECT DISTINCT group_id
FROM teaching_assignments
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE teachers.last_name = 'Фролов' --5


SELECT *
FROM subjects
WHERE specialty = 'АСОИ' --6

SELECT *
FROM teachers
WHERE specialty LIKE '%АСОИ%' --7


SELECT DISTINCT teachers.last_name
FROM teaching_assignments
JOIN teachers ON teaching_assignments.teacher_id = teachers.teacher_id
WHERE classroom = 210 --8

SELECT subjects.subject_name, student_groups.group_name
FROM teaching_assignments
JOIN subjects ON teaching_assignments.subject_id = subjects.subject_id
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE classroom BETWEEN 100 AND 200 --9




SELECT SUM(student_count)
FROM student_groups
WHERE specialty = 'ЭВМ' --11

SELECT DISTINCT teacher_id
FROM teaching_assignments
JOIN student_groups ON teaching_assignments.group_id = student_groups.group_id
WHERE specialty = 'ЭВМ' --12

SELECT subject_id
FROM teaching_assignments
GROUP BY subject_id
HAVING COUNT(DISTINCT group_id) = (SELECT COUNT(*) FROM student_groups) --13


