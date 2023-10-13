-- SQL script that queries the metal_bands table
-- and lists bands based on Glamor rock main style ordered by longevity

SELECT DISTINCT band_name, IFNULL(split, 2022) - formed as life_span
FROM metal_bands WHERE FIND_IN_SET('Glam rock', style) ORDER BY lifespan DESC;
