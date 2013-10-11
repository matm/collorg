CREATE TABLE "collorg.application".goal (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.goal' CHECK( cog_fqtn = 'collorg.application.goal' ),
   name STRING NOT NULL,
   description WIKI,
   PRIMARY KEY( name )
) INHERITS( "collorg.core".base_table ) ;

