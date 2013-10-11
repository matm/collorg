CREATE TABLE "collorg.documentation".paragraph (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.documentation.paragraph'
      CHECK( cog_fqtn = 'collorg.documentation.paragraph' ),
   part_oid C_OID,
   FOREIGN KEY ( part_oid ) REFERENCES "collorg.documentation".part( cog_oid ),
   text WIKI NOT NULL
   -- modification_date, versioning, ...
)INHERITS("collorg.core".base_table);
