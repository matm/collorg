CREATE TABLE "collorg.group"."wg_template" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN DEFAULT 'collorg.group.wg_template'
      CHECK( cog_fqtn = 'collorg.group.wg_template' ),
   name STRING NOT NULL,
   PRIMARY KEY(name),
   -- + group charcteristics
   permanent bool
) INHERITS( "collorg.core".base_table ) ;

