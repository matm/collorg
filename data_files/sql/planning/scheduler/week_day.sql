-- AKA ordre du jour
CREATE TABLE "collorg.planning.scheduler".week_day (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn TEXT
      DEFAULT 'collorg.planning.scheduler.week_day'
      CHECK( cog_fqtn = 'collorg.planning.scheduler.week_day' ),
   num INT CHECK(num >= 0 and num <= 7) UNIQUE NOT NULL,
   name STRING CHECK(
      name IN ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
               'Friday', 'Saturday')),
   CHECK ( 
      (num = 0 AND name = 'Sunday') OR
      (num = 1 AND name = 'Monday') OR
      (num = 2 AND name = 'Tuesday') OR
      (num = 3 AND name = 'Wednesday') OR
      (num = 4 AND name = 'Thursday') OR
      (num = 5 AND name = 'Friday') OR
      (num = 6 AND name = 'Saturday')),
   PRIMARY KEY(name)
) INHERITS( "collorg.core".base_table );
