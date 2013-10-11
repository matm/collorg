CREATE TABLE "collorg.time".hour (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.time.hour'
      CHECK( cog_fqtn = 'collorg.time.hour' ),
   day C_OID NOT NULL,
   FOREIGN KEY(day) REFERENCES "collorg.time".day(cog_oid),
   num HOUR NOT NULL,
   PRIMARY KEY(day, num)
) INHERITS( "collorg.core".base_table );
