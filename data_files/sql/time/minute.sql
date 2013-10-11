CREATE TABLE "collorg.time".minute (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.time.minute'
      CHECK( cog_fqtn = 'collorg.time.minute' ),
   hour C_OID NOT NULL,
   FOREIGN KEY(hour) REFERENCES "collorg.time".hour(cog_oid),
   time_stamp TIMESTAMP(0),
   num MINUTE NOT NULL,
   PRIMARY KEY(hour, num)
) INHERITS( "collorg.core".base_table );
