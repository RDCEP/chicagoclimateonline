-- reference

ALTER TABLE reference
  ADD COLUMN search_vector tsvector;

CREATE INDEX reference_search_index
  ON reference
  USING gin(search_vector);

-- tag

ALTER TABLE tag
  ADD COLUMN search_vector tsvector;


CREATE INDEX tag_search_index
  ON tag
  USING gin(search_vector);


CREATE TRIGGER tag_search_update BEFORE
  UPDATE OR INSERT ON tag
  FOR EACH ROW
  EXECUTE PROCEDURE tsvector_update_trigger(
    "search_vector", "pg_catalog.english",
    "name"
);

-- author

ALTER TABLE author
  ADD COLUMN search_vector tsvector;

CREATE INDEX author_search_index
  ON author
  USING gin(search_vector);

CREATE TRIGGER author_search_update BEFORE
  UPDATE OR INSERT ON author
  FOR EACH ROW
  EXECUTE PROCEDURE tsvector_update_trigger(
    "search_vector", "pg_catalog.english",
    "first_name",
    "last_name"
);

UPDATE reference SET title=title;
UPDATE tag SET name=name;
UPDATE author SET first_name=first_name;