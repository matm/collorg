CREATE TABLE "collorg.event".agenda_item (
   cog_oid C_OID PRIMARY KEY,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.event.agenda_item'
      CHECK( cog_fqtn = 'collorg.event.agenda_item' ),
   title string,
   abstract wiki
) INHERITS( "collorg.core".base_table );
