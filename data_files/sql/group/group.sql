CREATE TABLE "collorg.group"."group" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.group.group'
      CHECK( cog_fqtn = 'collorg.group.group' ),
   name STRING NOT NULL,
   data C_OID NOT NULL,
   open boolean default 'f',
   FOREIGN KEY(data) REFERENCES "collorg.core".oid_table(cog_oid),
   PRIMARY KEY(name, data)
) INHERITS("collorg.core".base_table) ;

