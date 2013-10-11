CREATE TABLE "collorg.planning".reunion (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.planning.reunion'
      CHECK( cog_fqtn = 'collorg.planning.reunion' ),
   event C_OID PRIMARY KEY,
   FOREIGN KEY( event ) REFERENCES "collorg.planning".event( cog_oid )
) INHERITS( "collorg.core".base_table );
