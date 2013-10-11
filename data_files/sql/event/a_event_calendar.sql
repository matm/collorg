CREATE TABLE "collorg.event".a_event_calendar (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.event.a_event_calendar'
      CHECK( cog_fqtn = 'collorg.event.a_event_calendar' ),
   event C_OID,
   FOREIGN KEY(event) REFERENCES "collorg.event".event(cog_oid),
   calendar C_OID NOT NULL,
   FOREIGN KEY(calendar) REFERENCES "collorg.planning".calendar(cog_oid),
   editable STRING,
   original BOOL DEFAULT 'f',
   PRIMARY KEY(event, calendar)
) INHERITS( "collorg.core".base_table );
