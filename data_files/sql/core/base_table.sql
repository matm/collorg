CREATE TABLE "collorg.core".base_table (
   cog_oid C_OID UNIQUE NOT NULL, -- DEFAULT uuid_generate_v4(),
   cog_fqtn C_FQTN NOT NULL,
   cog_signature TEXT,
   cog_test BOOL DEFAULT 'f',
   cog_creat_date TIMESTAMP( 0 )
      DEFAULT ('now'::text)::timestamp(0) with time zone,
   cog_modif_date TIMESTAMP( 0 )
      DEFAULT ('now'::text)::timestamp(0) with time zone,
   cog_environment c_oid references "collorg.core".oid_table(cog_oid),
   cog_state TEXT,
   PRIMARY KEY(cog_oid, cog_fqtn)
);

--CREATE UNIQUE INDEX cog_oid_cog_base_table_idx
--   ON "collorg.core".base_table( cog_oid, cog_salt ) ;
CREATE UNIQUE INDEX cog_oid_cog_base_table_idx
   ON "collorg.core".base_table( cog_oid ) ;
CREATE UNIQUE INDEX signature_base_table_idx
   ON "collorg.core".base_table( cog_signature ) ;
