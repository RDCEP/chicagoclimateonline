-- Add NL search to topics table

ALTER TABLE topics
  ADD COLUMN search_vector tsvector;

CREATE INDEX topics_search_index
  ON topics
  USING gin(search_vector);

CREATE TRIGGER topics_search_update BEFORE
  UPDATE OR INSERT ON topics
  FOR EACH ROW
  EXECUTE PROCEDURE tsvector_update_trigger("search_vector", "pg_catalog.english", "text", "title");
