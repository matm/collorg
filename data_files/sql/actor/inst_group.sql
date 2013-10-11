CREATE TABLE "collorg.actor"."inst_group" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.actor.inst_group'
      CHECK( cog_fqtn = 'collorg.actor.inst_group' ),
   name STRING NOT NULL,
   long_name STRING NOT NULL,
   advertise BOOL DEFAULT 'f',
   data_type c_fqtn NOT NULL,
   FOREIGN KEY (data_type) REFERENCES "collorg.core".data_type(fqtn),
   PRIMARY KEY(name, data_type)
) INHERITS( "collorg.actor"."actor" ) ;

