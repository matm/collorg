CREATE TABLE "collorg.core".namespace (
    cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
    cog_fqtn C_FQTN
       DEFAULT 'collorg.core.namespace' CHECK( cog_fqtn = 'collorg.core.namespace' ),
    database C_OID NOT NULL,
    FOREIGN KEY( database ) REFERENCES "collorg.core".database( cog_oid ),
    name STRING,
    description WIKI,
    PRIMARY KEY( name, database )
) INHERITS( "collorg.core".base_table );
