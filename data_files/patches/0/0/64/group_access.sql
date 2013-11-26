CREATE TABLE "collorg.access".group_access (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN 
        DEFAULT 'collorg.access.group_access'
        CHECK(cog_fqtn = 'collorg.access.group_access'),
   group_data C_OID NOT NULL REFERENCES "collorg.core".oid_table(cog_oid),
   accessed_data C_OID NOT NULL REFERENCES "collorg.core".oid_table(cog_oid),
   begin_date TIMESTAMP(0) DEFAULT ('now'::text)::timestamp(0) with time zone,
   end_date TIMESTAMP(0),
   write boolean default 'f',
   PRIMARY KEY(group_data, accessed_data, begin_date)
)INHERITS("collorg.core".base_table, "collorg.time".duration);
