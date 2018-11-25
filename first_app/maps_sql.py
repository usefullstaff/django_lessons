			
found_in_radius = """
SELECT name, ST_AsEWKT(point) 
FROM cafes 
WHERE ST_DWithin(point,
				ST_GeomFromEWKT('SRID=4326;POINT({:f} {:f})'),
				{:f});
"""