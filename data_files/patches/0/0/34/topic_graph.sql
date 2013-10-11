CREATE TABLE "collorg.web".topic_graph (
   topic c_oid NOT NULL,
   constraint "topic"
   FOREIGN KEY (topic) REFERENCES "collorg.web".topic(cog_oid),
   parent C_OID,
   constraint "parent"
   FOREIGN KEY (parent) REFERENCES "collorg.web".topic(cog_oid),
   "order" INT,
   PRIMARY KEY(topic, parent)
);
