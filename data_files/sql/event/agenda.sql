-- AKA ordre du jour
CREATE TABLE "collorg.event".agenda (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.event.agenda'
      CHECK( cog_fqtn = 'collorg.event.agenda' ),
   event C_OID PRIMARY KEY,
   FOREIGN KEY( event ) REFERENCES "collorg.event".event( cog_oid )
) INHERITS( "collorg.core".base_table );
