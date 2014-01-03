create table "collorg.communication".last_visited (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.last_visited'
      CHECK( cog_fqtn = 'collorg.communication.last_visited' ),
   "user" C_OID NOT NULL,
   FOREIGN KEY ("user") REFERENCES "collorg.actor"."user"( cog_oid ),
   "data" C_OID NOT NULL,
   FOREIGN KEY ("data") REFERENCES "collorg.core".oid_table( cog_oid ),
   PRIMARY KEY("user", data)
)INHERITS("collorg.core".base_table);
