CREATE TABLE "collorg.access".a_group_data (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN 
        DEFAULT 'collorg.access.a_group_data'
        CHECK(cog_fqtn = 'collorg.access.a_group_data'),
   "group" C_OID NOT NULL,
   FOREIGN KEY ("group") REFERENCES "collorg.group"."group"(cog_oid),
   data C_OID NOT NULL,
   FOREIGN KEY (data) REFERENCES "collorg.core".oid_table(cog_oid),
   begin_date TIMESTAMP(0) DEFAULT ('now'::text)::timestamp(0) with time zone,
   end_date TIMESTAMP(0),
   granted_by C_OID NOT NULL,
   FOREIGN KEY (granted_by) REFERENCES "collorg.actor"."user"(cog_oid),
   PRIMARY KEY("group", data)
)INHERITS("collorg.core".base_table);
