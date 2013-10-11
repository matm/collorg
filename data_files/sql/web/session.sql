CREATE TABLE "collorg.web".session (
   key C_OID PRIMARY KEY,
   creation_date TIMESTAMP(0)
      DEFAULT ('now'::text)::timestamp(0) with time zone,
   last_access_date TIMESTAMP(0),
   lease_time INT4,
   ip_addr CIDR,
   "user" C_OID NOT NULL,
   FOREIGN KEY ( "user" ) REFERENCES "collorg.actor"."user"( cog_oid )
);
