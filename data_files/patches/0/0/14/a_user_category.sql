CREATE TABLE "collorg.actor".a_user_category (
   "user" C_OID NOT NULL,
   FOREIGN KEY( "user" ) REFERENCES "collorg.actor"."user"( cog_oid ),
   category C_OID NOT NULL,
   FOREIGN KEY( category ) REFERENCES "collorg.actor".category( cog_oid ),
   PRIMARY KEY( "user", category ),
   "begin" TIMESTAMP(0)
      DEFAULT ('now'::text)::timestamp(0) with time zone,
   "end" TIMESTAMP(0)
);
