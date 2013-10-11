CREATE TABLE "collorg.location".site (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.location.site'
      CHECK( cog_fqtn = 'collorg.location.site' ),
   name STRING PRIMARY KEY
) INHERITS( "collorg.core".base_table );
