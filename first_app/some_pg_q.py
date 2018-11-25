

SELECT * FROM pgr_dijkstra('SELECT osm_id, source, target, st_length(way) as cost FROM planet_osm_roads', 8158253, 8901796, false, false);


ALTER TABLE planet_osm_roads_vertices_pgr ALTER COLUMN  id TYPE Bigint;
ALTER TABLE planet_osm_roads ALTER COLUMN  osm_id TYPE Bigint;
pgr_dijkstra(TEXT edges_sql, BIGINT start_vid, BIGINT end_vid)




SELECT * FROM pgr_dijkstra('SELECT osm_id as id, source, target, st_length(way) as cost FROM planet_osm_roads', 547504168, 547504159, directed := false);


SELECT * FROM pgr_dijkstra('SELECT osm_id as id, source, target, st_length(way) as cost FROM planet_osm_roads', 547504168, 547504159, directed := true);



SELECT * FROM pgr_dijkstra('SELECT id as id, source, target, st_length(the_geom) as cost FROM planet_osm_roads_vertices_pgr', 1901, 1936, directed := false);


