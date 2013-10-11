CREATE TABLE "collorg.access".indirect (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.access.indirect'
      CHECK( cog_fqtn = 'collorg.access.indirect' ),
   "granted" C_OID NOT NULL,
   FOREIGN KEY("granted") REFERENCES "collorg.core".oid_table(cog_oid),
   grants C_OID NOT NULL,
   FOREIGN KEY(grants) REFERENCES "collorg.core".oid_table( cog_oid ),
   PRIMARY KEY("granted", grants )
) INHERITS( "collorg.core".base_table ) ;
