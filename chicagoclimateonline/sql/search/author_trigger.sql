DROP TRIGGER author_search_update ON author;
DROP FUNCTION author_before_update() CASCADE;
DROP FUNCTION author_after_update() CASCADE;


CREATE FUNCTION author_before_update()
  RETURNS TRIGGER AS $author_before_update$

  BEGIN

    NEW.search_vector := setweight(to_tsvector('english', NEW.first_name), 'A');
    NEW.search_vector := NEW.search_vector || setweight(to_tsvector('english', NEW.last_name), 'A');

    RETURN NEW;

  END;
  $author_before_update$ LANGUAGE plpgsql;


CREATE TRIGGER author_before_update
  BEFORE UPDATE OR INSERT on author
  FOR EACH ROW
  EXECUTE PROCEDURE author_before_update();


CREATE FUNCTION author_after_update()
  RETURNS TRIGGER AS $author_after_update$

  DECLARE
    r_row       record;
    ref_vector  tsvector;
    tag_vector  tsvector;
    auth_vector tsvector;

  BEGIN

    auth_vector := ''::tsvector;
    tag_vector := ''::tsvector;

    FOR r_row IN SELECT * FROM reference
      WHERE id IN (SELECT reference_id FROM reference_author
        WHERE author_id IN (SELECT id FROM author WHERE id=NEW.id))
    LOOP
      -- UPDATE reference row
      UPDATE reference SET title=r_row.title WHERE id=r_row.id;
    END LOOP;

    RETURN NEW;
  END;
  $author_after_update$ LANGUAGE plpgsql;


CREATE TRIGGER author_after_update
  AFTER UPDATE OR INSERT on author
  FOR EACH ROW
  EXECUTE PROCEDURE author_after_update();


