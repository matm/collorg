CREATE TABLE "collorg.core".field (
    cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
    cog_fqtn C_FQTN
       DEFAULT 'collorg.core.field' CHECK( cog_fqtn = 'collorg.core.field' ),
    data_type C_FQTN NOT NULL,
    FOREIGN KEY (data_type) REFERENCES "collorg.core"."data_type"(fqtn) ON UPDATE CASCADE,
    fqfn STRING,
    label STRING,
    status STRING DEFAULT 'private'
       CHECK( status = 'public' OR
              status = 'protected' OR
              status = 'private' ),
    description WIKI,
    PRIMARY KEY(fqfn) 
) INHERITS( "collorg.core".base_table );
