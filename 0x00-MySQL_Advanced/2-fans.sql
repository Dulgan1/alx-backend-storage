-- SQL script queries amd ranks bands by number of fans
-- By column names origin, fans as nb_fans at table metal_bands

SELECT DISTINCT origin, SUM(fans) AS nb_fans FROM metal_bands GROUP BY origin
ORDER BY nb_fans DESC;
