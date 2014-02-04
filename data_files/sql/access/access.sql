CREATE TABLE "collorg.access".access (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
        DEFAULT 'collorg.access.access'
        CHECK(cog_fqtn = 'collorg.access.access'),
   "user" C_OID NOT NULL,
   constraint "user"
   FOREIGN KEY ("user") REFERENCES "collorg.actor"."user"(cog_oid),
   data C_OID NOT NULL,
   constraint "data"
   FOREIGN KEY (data) REFERENCES "collorg.core".oid_table(cog_oid),
   write boolean default 'f',
   manage boolean default 'f',
   begin_date TIMESTAMP(0) DEFAULT ('now'::text)::timestamp(0) with time zone,
   end_date TIMESTAMP(0),
   description WIKI,
   pourcentage INT CHECK (pourcentage <= 100),
   PRIMARY KEY("user", data, begin_date)
)INHERITS("collorg.core".base_table, "collorg.time".duration);
