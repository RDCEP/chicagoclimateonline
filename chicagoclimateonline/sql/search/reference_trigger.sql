DROP FUNCTION reference_before_update() CASCADE;
DROP FUNCTION reference_after_update() CASCADE;


CREATE FUNCTION reference_before_update()
  RETURNS TRIGGER AS $reference_before_update$

  BEGIN

    NEW.search_vector := setweight(to_tsvector('english', NEW.title), 'A');
    NEW.search_vector := NEW.search_vector || setweight(to_tsvector('english', NEW.publisher), 'B');
    NEW.search_vector := NEW.search_vector || setweight(to_tsvector('english', NEW.publication), 'B');
    NEW.search_vector := NEW.search_vector || to_tsvector('english', NEW.journal_abbr);
    NEW.search_vector := NEW.search_vector || setweight(to_tsvector('english', NEW.book_title), 'A');

    RETURN NEW;

  END;
  $reference_before_update$ LANGUAGE plpgsql;



CREATE TRIGGER reference_before_update
  BEFORE UPDATE OR INSERT on reference
  FOR EACH ROW
  EXECUTE PROCEDURE reference_before_update();


CREATE FUNCTION reference_after_update()
  RETURNS TRIGGER AS $reference_after_update$

  DECLARE
    trow        record;
    arow        record;
    ref_vector  tsvector;
    tag_vector  tsvector;
    auth_vector tsvector;

  BEGIN

    auth_vector := ''::tsvector;
    tag_vector := ''::tsvector;

    FOR trow IN SELECT * FROM tag
      WHERE id IN (SELECT tag_id FROM reference_tag
        WHERE reference_id IN (SELECT id FROM reference WHERE id=NEW.id))
    LOOP
      tag_vector := tag_vector || trow.search_vector;
    END LOOP;

    FOR arow IN SELECT search_vector FROM author
    WHERE id IN (SELECT author_id FROM reference_author
      WHERE reference_id IN (SELECT id FROM reference WHERE id=NEW.id))
    LOOP
      auth_vector := auth_vector || arow.search_vector;
    END LOOP;

    NEW.search_vector := NEW.search_vector || auth_vector;
    NEW.search_vector := NEW.search_vector || tag_vector;

    RETURN NEW;
  END;
  $reference_after_update$ LANGUAGE plpgsql;



CREATE TRIGGER reference_after_update
  AFTER UPDATE OR INSERT on reference
  FOR EACH ROW
  EXECUTE PROCEDURE reference_after_update();



-- UPDATE reference SET title='Foo 3' WHERE id=1;


-- SELECT search_vector FROM reference;