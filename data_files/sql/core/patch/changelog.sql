CREATE SCHEMA "collorg.core.patch";
CREATE TABLE "collorg.core.patch".changelog (
    cog_oid C_OID UNIQUE NOT NULL,
    FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
       INITIALLY DEFERRED,
    cog_fqtn C_FQTN
       DEFAULT 'collorg.core.patch.changelog'
       CHECK( cog_fqtn = 'collorg.core.patch.changelog' ),
    major INT DEFAULT 0,
    minor INT DEFAULT 0,
    stage INT DEFAULT 0 CHECK (stage IN (0, 1, 2, 3, 4)),
    -- ['alpha', 'beta', 'release candidate', 'release', 'unsupported']
    revision INT DEFAULT 0,
    database C_OID NOT NULL,
    FOREIGN KEY(database) REFERENCES "collorg.core".database(cog_oid),
    label STRING NOT NULL,
    description WIKI,
    "output" TEXT,
    "error" TEXT,
    PRIMARY KEY(major, minor, stage, revision, database)
) INHERITS("collorg.core".base_table);
