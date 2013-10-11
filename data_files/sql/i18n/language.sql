CREATE TABLE "collorg.i18n".language (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.i18n.language' CHECK( cog_fqtn = 'collorg.i18n.language' ),
   name STRING NOT NULL,
   encoding STRING NOT NULL DEFAULT( 'utf-8' ),
   PRIMARY KEY( name )
) INHERITS( "collorg.core".base_table ) ;

