

SELECT * FROM pgr_dijkstra('SELECT osm_id, source, target, st_length(way) as cost FROM planet_osm_roads', 8158253, 8901796, false, false);


ALTER TABLE planet_osm_roads_vertices_pgr ALTER COLUMN  id TYPE Bigint;
ALTER TABLE planet_osm_roads ALTER COLUMN  osm_id TYPE Bigint;
pgr_dijkstra(TEXT edges_sql, BIGINT start_vid, BIGINT end_vid)


https://docs.pgrouting.org/2.0/en/src/common/doc/functions/create_vert_table.html - о сурс и таргет
https://docs.pgrouting.org/2.6/en/pgRouting-concepts.html#description-of-the-edges-sql-query-for-dijkstra-like-functions

SELECT * FROM pgr_dijkstra('SELECT osm_id AS id, source, target, st_length(way) as cost FROM planet_osm_roads', 4419539, 8599729);


SELECT * FROM pgr_dijkstra('SELECT osm_id AS id, source, target, st_length(way) as cost FROM planet_osm_roads', 8599729, 4419539,  false);

planet_osm_roads_vertices_pgr