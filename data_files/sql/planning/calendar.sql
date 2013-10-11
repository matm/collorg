CREATE TABLE "collorg.planning".calendar (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.planning.calendar'
      CHECK( cog_fqtn = 'collorg.planning.calendar' ),
   "group" C_OID NOT NULL,
   FOREIGN KEY("group") REFERENCES "collorg.group"."group"(cog_oid),
   PRIMARY KEY("group")
) INHERITS( "collorg.core".base_table );
