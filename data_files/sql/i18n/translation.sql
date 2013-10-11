CREATE TABLE "collorg.i18n".translation (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.i18n.translation' CHECK( cog_fqtn = 'collorg.i18n.translation' ),
   data_oid C_OID NOT NULL,
   FOREIGN KEY( data_oid ) REFERENCES "collorg.core".oid_table( cog_oid ),
   language C_OID,
   FOREIGN KEY( language ) REFERENCES "collorg.i18n".language( cog_oid ),
   field STRING NOT NULL,
   FOREIGN KEY( field ) REFERENCES "collorg.core".field(fqfn),
   translation STRING NOT NULL,
   PRIMARY KEY( data_oid, field, language )
) INHERITS( "collorg.core".base_table ) ;
