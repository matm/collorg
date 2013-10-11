CREATE TABLE "collorg.web".url (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.web.url' CHECK( cog_fqtn = 'collorg.web.url' ),
   name URL NOT NULL,
   label STRING,
   data C_OID NOT NULL,
   FOREIGN KEY( data ) REFERENCES "collorg.core".oid_table( cog_oid ),
   language C_OID,
   action C_OID NOT NULL,
   FOREIGN KEY( action ) REFERENCES "collorg.application".action( cog_oid ),
   FOREIGN KEY( language ) REFERENCES "collorg.i18n".language( cog_oid ),
   PRIMARY KEY( name )
) INHERITS( "collorg.core".base_table ) ;
