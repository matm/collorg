CREATE TABLE "collorg.location".building (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.location.building'
      CHECK( cog_fqtn = 'collorg.location.building' ),
   name STRING,
   site C_OID,
   foreign key(site) references "collorg.location".site(cog_oid),
   address C_OID,
   foreign key(address) references "collorg.location".address(cog_oid)
) INHERITS( "collorg.core".base_table );
