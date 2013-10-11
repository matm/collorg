CREATE TABLE "collorg.core"."data_type" (
    cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
    cog_fqtn C_FQTN
       DEFAULT 'collorg.core.data_type' CHECK( cog_fqtn = 'collorg.core.data_type' ),
    namespace C_OID NOT NULL,
    FOREIGN KEY( namespace )
        REFERENCES "collorg.core".namespace( cog_oid ) DEFERRABLE,
    name STRING,
    fqtn TEXT UNIQUE NOT NULL,
    description WIKI,
    PRIMARY KEY( namespace, name )
) INHERITS( "collorg.core".base_table );
