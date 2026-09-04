SELECT DISTINCT parts.color
FROM spj
JOIN parts ON spj.part_id = parts.part_id
WHERE spj.supplier_id = 'П1'; --20


SELECT project_name
FROM spj
JOIN projects ON spj.project_id = projects.project_id
WHERE spj.supplier_id = 'П1'; --19


SELECT DISTINCT spj.supplier_id
FROM spj
WHERE spj.part_id IN (
    SELECT part_id
    FROM spj
    WHERE supplier_id IN (
        SELECT supplier_id
        FROM spj 
        WHERE part_id IN (
            SELECT part_id
            FROM parts
            WHERE color = 'Красный'
        )
    )
); --23


SELECT project_id
FROM projects
WHERE project_id NOT IN (
    SELECT project_id 
    FROM spj
    WHERE part_id IN (
        SELECT part_id
        FROM parts WHERE color = 'Красный'
    ) 
    AND supplier_id IN (
        SELECT supplier_id
        FROM suppliers
        WHERE city = 'Лондон'
    )
);   --28


SELECT DISTINCT color, city
FROM parts; --5


SELECT suppliers.supplier_id, parts.part_id, projects.project_id
FROM suppliers, parts, projects
WHERE suppliers.city = parts.city AND parts.city = projects.city; --6


SELECT part_id
FROM spj
WHERE supplier_id IN (
    SELECT supplier_id
    FROM suppliers 
    WHERE city = 'Лондон'
)
AND project_id IN (
    SELECT project_id
    FROM projects
    WHERE city = 'Лондон'
); --10


SELECT DISTINCT a.part_id, b.part_id
FROM spj AS a
JOIN spj AS b on a.supplier_id = b.supplier_id
WHERE a.part_id < b.part_id; --14


SELECT DISTINCT part_id 
FROM spj
JOIN projects ON spj.project_id = projects.project_id
JOIN suppliers ON spj.supplier_id = suppliers.supplier_id
WHERE suppliers.city = 'Лондон' OR projects.city = 'Лондон'; --34


SELECT suppliers.supplier_id, parts.part_id
FROM suppliers, parts
EXCEPT
SELECT supplier_id, part_id 
FROM spj;

