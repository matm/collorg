CREATE TABLE "collorg.planning".task (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.planning.task'
      CHECK( cog_fqtn = 'collorg.planning.task' ),
   name STRING,
   description TEXT,
   PRIMARY KEY(name)
) INHERITS( "collorg.core".base_table );
