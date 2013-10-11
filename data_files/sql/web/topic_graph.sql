CREATE TABLE "collorg.web".topic_graph (
   topic c_oid NOT NULL,
   constraint "topic"
   FOREIGN KEY (topic) REFERENCES "collorg.web".topic(cog_oid),
   parent C_OID,
   constraint "parent"
   FOREIGN KEY (parent) REFERENCES "collorg.core".oid_table(cog_oid),
   "order" INT,
   link boolean default 'f',
   PRIMARY KEY(topic, parent)
);
