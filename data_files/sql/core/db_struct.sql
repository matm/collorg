CREATE VIEW "collorg.core".db_struct AS
SELECT
a.attrelid AS tableid,
    array_agg( i.inhseqno::TEXT || ':' || i.inhparent::TEXT ),
--    db.datname AS database_name,
--    db.encoding AS database_encoding,
    c.relkind AS tablekind,
    n.nspname AS schemaname,
    c.relname AS tablename,
    a.attname AS fieldname,
    a.attndims AS fielddim,
    pt.typname AS fieldtype,
    a.attnum AS fieldnum,
        NOT( a.attislocal ) AS inherited,
    cn_uniq.contype AS uniq,
    a.attnotnull OR NULL AS notnull,
    cn_pk.contype AS pkey,
    cn_fk.contype AS fkey,
    cn_fk.conname AS fkeyname,
    cn_fk.conkey AS keynum,
    cn_fk.confrelid AS fkeytableid,
    cn_fk.confkey AS fkeynum,
    -- mettre le nom de la clef référencée en clair
    n_fk.nspname AS fk_schemaname,
    c_fk.relname AS fk_tablename,
    a_fk.attname AS fk_fieldname
FROM
    pg_class c -- table
    LEFT JOIN pg_namespace n ON
    n.oid = c.relnamespace
--    LEFT JOIN pg_tablespace t ON
--    t.oid = c.reltablespace
--    JOIN pg_database db ON
--    db.dattablespace = t.oid
    LEFT JOIN pg_inherits i ON
    i.inhrelid = c.oid
    LEFT JOIN pg_attribute a ON
    a.attrelid = c.oid
    JOIN pg_type pt ON
    a.atttypid = pt.oid
    LEFT JOIN pg_constraint cn_uniq ON
    cn_uniq.contype = 'u' AND
    cn_uniq.conrelid = a.attrelid AND
    a.attnum = ANY( cn_uniq.conkey )
    LEFT JOIN pg_constraint cn_pk ON
    cn_pk.contype = 'p' AND
    cn_pk.conrelid = a.attrelid AND
    a.attnum = ANY( cn_pk.conkey )
    LEFT JOIN pg_constraint cn_fk ON
    cn_fk.contype = 'f' AND
    cn_fk.conrelid = a.attrelid AND
    a.attnum = ANY( cn_fk.conkey )
    -- les réf. clef étrangères en clair
    LEFT JOIN pg_class c_fk ON
    c_fk.oid = cn_fk.confrelid
    LEFT JOIN pg_namespace n_fk ON
    n_fk.oid = c_fk.relnamespace
    LEFT JOIN pg_attribute a_fk ON
    a_fk.attrelid = c_fk.oid AND
    a_fk.attnum = cn_fk.confkey[idx( cn_fk.conkey, a.attnum )]
WHERE
    n.nspname <> 'pg_catalog'::name AND
    n.nspname <> 'information_schema'::name AND
    ( c.relkind = 'r'::"char" OR c.relkind = 'v'::"char" ) AND
    a.attnum > 0
GROUP BY
    a.attrelid,
--    db.datname,
--    db.encoding,
    n.nspname,
    c.relname,
    c.relkind,
    a.attnum,
    a.attname,
    a.attndims,
    a.attislocal,
    pt.typname,
    cn_uniq.contype,
    a.attnotnull,
    cn_pk.contype,
    cn_fk.contype,
    cn_fk.conname,
    cn_fk.conkey,
    cn_fk.confrelid,
    cn_fk.confkey,
    n_fk.nspname,
    c_fk.relname,
    a_fk.attname
ORDER BY
    a.attrelid,
    c.relkind,
    a.attnum, n.nspname, c.relname ;
