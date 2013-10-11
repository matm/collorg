CREATE TABLE "collorg.activity".goal (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.activity.goal'
      CHECK( cog_fqtn = 'collorg.activity.goal' ),
   name STRING NOT NULL,
   description WIKI,
   PRIMARY KEY( name )
) INHERITS( "collorg.core".base_table ) ;

