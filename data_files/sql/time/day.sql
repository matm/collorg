CREATE TABLE "collorg.time".day (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.time.day'
      CHECK( cog_fqtn = 'collorg.time.day' ),
   month C_OID NOT NULL,
   FOREIGN KEY(month) REFERENCES "collorg.time".month(cog_oid),
   num DAY NOT NULL,
   PRIMARY KEY(month, num)
) INHERITS( "collorg.core".base_table );
