CREATE SCHEMA "collorg.event";
CREATE TABLE "collorg.event".event (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.event.event'
      CHECK( cog_fqtn = 'collorg.event.event' ),
   begin_date TIMESTAMP(0) NOT NULL,
   end_date TIMESTAMP(0) NOT NULL,
   location C_OID,
   FOREIGN KEY(location) REFERENCES "collorg.location".room(cog_oid),
   other_location WIKI,
   PRIMARY KEY(cog_oid)
) INHERITS( "collorg.communication.blog".post );
