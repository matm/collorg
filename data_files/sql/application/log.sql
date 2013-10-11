CREATE SEQUENCE "collorg.application".log_seq;
CREATE TABLE "collorg.application".log (
   id INTEGER PRIMARY KEY DEFAULT nextval('"collorg.application".log_seq'),
   "timestamp" TIMESTAMP( 0 )
      DEFAULT ('now'::text)::timestamp(0) with time zone,
   action C_OID NOT NULL,
   FOREIGN KEY( action ) REFERENCES "collorg.application".action( cog_oid ),
   data_oid C_OID,
   FOREIGN KEY( data_oid ) REFERENCES "collorg.core".oid_table( cog_oid ),
   transition C_OID,
   FOREIGN KEY( transition ) REFERENCES "collorg.application".transition( cog_oid ),
   state C_OID,
   FOREIGN KEY( state ) REFERENCES "collorg.application".state( cog_oid ),
   "user" C_OID,
   FOREIGN KEY( "user" ) REFERENCES "collorg.actor"."user"( cog_oid ),
   log_text TEXT
);
