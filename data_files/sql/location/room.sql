CREATE TABLE "collorg.location".room (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.location.room'
      CHECK( cog_fqtn = 'collorg.location.room' ),
   name STRING,
   building C_OID,
   foreign key(building) references "collorg.location".building(cog_oid),
   access WIKI
) INHERITS( "collorg.core".base_table );
