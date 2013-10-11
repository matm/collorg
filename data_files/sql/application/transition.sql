CREATE TABLE "collorg.application".transition (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.transition'
      CHECK( cog_fqtn = 'collorg.application.transition' ),
   name STRING NOT NULL,
   description WIKI,
   action C_OID NOT NULL,
   FOREIGN KEY( action ) REFERENCES "collorg.application".action( cog_oid ),
   start_state C_OID NOT NULL,
   FOREIGN KEY( start_state ) REFERENCES "collorg.application".state( cog_oid ),
   end_state C_OID NOT NULL,
   FOREIGN KEY( end_state ) REFERENCES "collorg.application".state( cog_oid ),
   PRIMARY KEY( start_state, end_state )
) INHERITS( "collorg.core".base_table ) ;

