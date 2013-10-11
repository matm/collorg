CREATE TABLE "collorg.planning.scheduler".month_day (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn TEXT
      DEFAULT 'collorg.planning.scheduler.month_day'
      CHECK( cog_fqtn = 'collorg.planning.scheduler.month_day' ),
   num INT CHECK(num >= 1 and num <= 31) UNIQUE NOT NULL,
   PRIMARY KEY(num)
) INHERITS( "collorg.core".base_table );
