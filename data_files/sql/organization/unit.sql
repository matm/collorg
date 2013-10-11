CREATE TABLE "collorg.organization".unit (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      CHECK( cog_fqtn != 'collorg.organzation.unit' ),
   acronym STRING,
   name STRING NOT NULL,
   description WIKI,
   url URL,
   PRIMARY KEY( cog_fqtn, name )
) INHERITS("collorg.core".base_table, "collorg.time".duration);

-- this is an abstract table
-- the actual organizational units must inherit from this table
