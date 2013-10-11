CREATE TABLE "collorg.event"."a_agenda_agenda_item" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.event.a_agenda_agenda_item'
      CHECK( cog_fqtn = 'collorg.event.a_agenda_agenda_item' ),
   agenda C_OID NOT NULL,
   FOREIGN KEY(agenda) REFERENCES "collorg.event"."agenda"(cog_oid),
   agenda_item C_OID NOT NULL,
   FOREIGN KEY(agenda_item) REFERENCES "collorg.event"."agenda_item"(cog_oid),
   PRIMARY KEY(agenda, agenda_item)
) INHERITS( "collorg.core".base_table ) ;

