CREATE TABLE "collorg.application".domain (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.domain' CHECK( cog_fqtn = 'collorg.application.domain' ),
   name STRING NOT NULL,
   description WIKI,
   PRIMARY KEY( name )
) INHERITS( "collorg.core".base_table ) ;

