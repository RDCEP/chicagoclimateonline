DROP FUNCTION tags_before_update() CASCADE;
DROP FUNCTION tags_after_update() CASCADE;


CREATE FUNCTION tags_before_update()
  RETURNS TRIGGER AS $tags_before_update$

  BEGIN

    IF TG_OP = 'INSERT' THEN
      NEW.search_vector = setweight(to_tsvector('pg_catalog.english', COALESCE(NEW.name, '')), 'A');
    END IF;
    IF TG_OP = 'UPDATE' THEN
      IF NEW.name <> OLD.name THEN
        NEW.search_vector = setweight(to_tsvector('pg_catalog.english', COALESCE(NEW.name, '')), 'A');
      END IF;
    END IF;

    RETURN NEW;

  END;
  $tags_before_update$ LANGUAGE plpgsql;


CREATE TRIGGER tags_before_update
  BEFORE UPDATE OR INSERT on tag
  FOR EACH ROW
  EXECUTE PROCEDURE tags_before_update();


CREATE FUNCTION tags_after_update()
  RETURNS TRIGGER AS $tags_after_update$

  DECLARE
    r_row       record;
    ref_vector  tsvector;
    tag_vector  tsvector;
    auth_vector tsvector;

  BEGIN

    auth_vector := ''::tsvector;
    tag_vector := ''::tsvector;

    -- NEW.search_vector := to_tsvector('english', NEW.name);

    FOR r_row IN SELECT * FROM reference
      WHERE id IN (SELECT reference_id FROM reference_tag
        WHERE tag_id IN (SELECT id FROM tag WHERE id=NEW.id))
    LOOP
      -- UPDATE reference row
      UPDATE reference SET title=r_row.title WHERE id=r_row.id;
    END LOOP;

    RETURN NEW;
  END;
  $tags_after_update$ LANGUAGE plpgsql;


CREATE TRIGGER tags_after_update
  AFTER UPDATE OR INSERT on tag
  FOR EACH ROW
  EXECUTE PROCEDURE tags_after_update();