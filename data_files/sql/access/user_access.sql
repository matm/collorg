CREATE TABLE "collorg.access".access (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
        DEFAULT 'collorg.access.access'
        CHECK(cog_fqtn = 'collorg.access.access'),
   grant_date TIMESTAMP(0)
      DEFAULT ('now'::text)::timestamp(0) with time zone,
   "user" C_OID,
   FOREIGN KEY ( "user" ) REFERENCES "collorg.actor"."user"( cog_oid ),
   group C_OID,
   FOREIGN KEY ( group ) REFERENCES "collorg.group".group( cog_oid ),
   role C_OID NOT NULL,
   FOREIGN KEY ( role ) REFERENCES "collorg.actor".role( cog_oid ),
   begin_date TIMESTAMP(0),
   end_date TIMESTAMP(0),
   description WIKI,
   PRIMARY KEY( "user", group, role )
)INHERITS("collorg.core".base_table);
