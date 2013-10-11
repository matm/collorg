CREATE TABLE "collorg.web".rss (
   key C_OID UNIQUE NOT NULL,
   "user" c_oid,
   CONSTRAINT "user"
     FOREIGN KEY("user") REFERENCES "collorg.core".oid_table(cog_oid),
   title string,
   description text,
   PRIMARY KEY("user", title)
);
