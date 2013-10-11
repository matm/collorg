CREATE TABLE "collorg.documentation".part (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.documentation.part'
      CHECK( cog_fqtn = 'collorg.documentation.part' ),
   part_type STRING CHECK( part_type IN ( 'part', 'section', 'subsection' ) ),
   part_number TEXT, -- 0, 1, 1.1, 1.1.1, pour l'ordre des parties
   title STRING NOT NULL,
   document C_OID NOT NULL,
   FOREIGN KEY( document ) REFERENCES "collorg.documentation".document( cog_oid ),
   summary WIKI
   -- date de création, versioning, ...
)INHERITS("collorg.core".base_table);
