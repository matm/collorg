CREATE TABLE "collorg.time".month (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.time.month'
      CHECK( cog_fqtn = 'collorg.time.month' ),
   year C_OID NOT NULL,
   FOREIGN KEY(year) REFERENCES "collorg.time".year(cog_oid),
   num MONTH NOT NULL,
   PRIMARY KEY(year, num)
) INHERITS( "collorg.core".base_table );
