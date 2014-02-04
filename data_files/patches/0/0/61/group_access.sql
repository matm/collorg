CREATE TABLE "collorg.access".group_access (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
        DEFAULT 'collorg.access.group_access'
        CHECK(cog_fqtn = 'collorg.access.group_access'),
   "group" C_OID NOT NULL,
   constraint "group"
   FOREIGN KEY ("group") REFERENCES "collorg.group"."group"(cog_oid),
   data C_OID NOT NULL,
   constraint "data"
   FOREIGN KEY (data) REFERENCES "collorg.core".oid_table(cog_oid),
   write boolean default 'f',
   manage boolean default 'f',
   description WIKI,
   PRIMARY KEY("group", data, cog_from)
)INHERITS("collorg.core".base_table, "collorg.time".duration);
