-- Aggregate view for NL search

CREATE OR REPLACE VIEW search AS
  SELECT reference.abstract AS text,
         reference.title AS title,
         reference.search_vector AS search_vector,
         'reference' as object,
         reference.id as object_id,
         reference.id as id
    FROM reference
  UNION ALL
  SELECT topic.text AS text,
         topic.name AS title,
         topic.search_vector AS search_vector,
         'topic' as object,
         topic.id as object_id,
         topic.id as id
    FROM topic