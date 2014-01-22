CREATE TABLE "collorg.application".task (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.task' CHECK( cog_fqtn = 'collorg.application.task' ),
   name STRING primary key,
   delegable BOOLEAN DEFAULT 'f',
   description WIKI
) INHERITS( "collorg.core".base_table, "collorg.time".duration ) ;
