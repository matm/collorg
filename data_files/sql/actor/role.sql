CREATE TABLE "collorg.actor".role (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.actor.role'
      CHECK( cog_fqtn = 'collorg.actor.role' ),
   "function" C_OID NOT NULL,
   FOREIGN KEY( "function" ) REFERENCES "collorg.actor"."function"(cog_oid),
   "data" C_OID NOT NULL,
   FOREIGN KEY( "data" ) REFERENCES "collorg.core"."oid_table"(cog_oid),
   PRIMARY KEY( "function", "data" )
) INHERITS( "collorg.actor"."actor" ) ;
