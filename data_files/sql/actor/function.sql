CREATE TABLE "collorg.actor"."function" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.actor.function'
      CHECK( cog_fqtn = 'collorg.actor.function' ),
   name STRING NOT NULL,
   fname STRING NOT NULL,
   long_name STRING UNIQUE NOT NULL,
   advertise BOOL DEFAULT 'f',
   "data_type" C_FQTN NOT NULL,
   FOREIGN KEY( "data_type" ) REFERENCES "collorg.core"."data_type"(fqtn) ON UPDATE CASCADE,
   UNIQUE(name, data_type),
   PRIMARY KEY(long_name)
) INHERITS( "collorg.actor"."actor" ) ;

