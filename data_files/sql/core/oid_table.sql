CREATE TABLE "collorg.core".oid_table (
    cog_oid C_OID UNIQUE NOT NULL,
    cog_fqtn C_FQTN NOT NULL,
    --CONSTRAINT fk_table FOREIGN KEY ( cog_fqtn )
    --    REFERENCES "collorg.core"."data_type"( fqtn ) DEFERRABLE,
    --cog_label STRING DEFAULT '',
    PRIMARY KEY( cog_oid, cog_fqtn )
) ;

-- removed est mis à true pour faire le ménage en différé
