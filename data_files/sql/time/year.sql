CREATE TABLE "collorg.time".year (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.time.year'
      CHECK( cog_fqtn = 'collorg.time.year' ),
   num INT PRIMARY KEY
) INHERITS( "collorg.core".base_table );
