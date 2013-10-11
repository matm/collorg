CREATE TABLE "collorg.communication.blog".a_post_group (
post C_OID NOT NULL,
FOREIGN KEY(post) REFERENCES "collorg.core".oid_table(cog_oid),
"group" C_OID NOT NULL,
FOREIGN KEY("group") REFERENCES "collorg.group"."group"(cog_oid),
comment_enabled BOOL DEFAULT 'f',
write BOOL DEFAULT 'f',
PRIMARY KEY(post, "group")
);
