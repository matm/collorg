CREATE TABLE "collorg.web".wall (
   topic c_oid NOT NULL,
   constraint "topic"
   FOREIGN KEY (topic) REFERENCES "collorg.web".topic(cog_oid),
   parent C_OID,
   constraint "parent"
   FOREIGN KEY (parent) REFERENCES "collorg.web".topic(cog_oid),
   PRIMARY KEY(topic, parent)
);
