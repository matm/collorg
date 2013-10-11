CREATE TABLE "collorg.activity".task (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.activity.task'
      CHECK( cog_fqtn = 'collorg.activity.task' ),
   name STRING NOT NULL,
   delegable BOOLEAN DEFAULT 'f',
   description WIKI,
   PRIMARY KEY( name )
) INHERITS( "collorg.core".base_table ) ;
