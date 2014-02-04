CREATE SCHEMA "collorg.planning.scheduler";
-- AKA ordre du jour
CREATE TABLE "collorg.planning.scheduler".month (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn TEXT
      DEFAULT 'collorg.planning.scheduler.month'
      CHECK( cog_fqtn = 'collorg.planning.scheduler.month' ),
   num INT CHECK(num >= 1 and num <= 12) UNIQUE NOT NULL,
   name STRING CHECK(
      name IN ('January', 'February', 'March', 'April', 'May', 'June',
         'July', 'August', 'September', 'October', 'November', 'December')),
   CHECK (
      (num = 1 AND name = 'January') OR
      (num = 2 AND name = 'February') OR
      (num = 3 AND name = 'March') OR
      (num = 4 AND name = 'April') OR
      (num = 5 AND name = 'May') OR
      (num = 6 AND name = 'June') OR
      (num = 7 AND name = 'July') OR
      (num = 8 AND name = 'August') OR
      (num = 9 AND name = 'September') OR
      (num = 10 AND name = 'October') OR
      (num = 11 AND name = 'November') OR
      (num = 12 AND name = 'December')),
   PRIMARY KEY(name)
) INHERITS( "collorg.core".base_table );
