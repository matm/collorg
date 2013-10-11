ALTER TABLE "collorg.actor".inst_group ADD column data_type c_fqtn ;
UPDATE "collorg.actor".inst_group SET data_type = sq.data_type FROM ( SELECT data_type, inst_group from "collorg.actor".function ) AS sq WHERE sq.inst_group = cog_oid;
DELETE FROM "collorg.actor".inst_group WHERE data_type is NULL;
ALTER TABLE "collorg.actor".inst_group ADD constraint data_type_fqtn_fkey FOREIGN KEY (data_type) REFERENCES "collorg.core".data_type(fqtn);
ALTER TABLE "collorg.actor".inst_group ALTER COLUMN data_type SET NOT NULL;
ALTER TABLE "collorg.actor".inst_group DROP CONSTRAINT inst_group_pkey;
ALTER TABLE "collorg.actor".inst_group ADD constraint inst_group_pkey PRIMARY KEY (name, data_type);

ALTER TABLE "collorg.actor".function DROP CONSTRAINT function_pkey;
ALTER TABLE "collorg.actor".function ADD constraint function_pkey PRIMARY KEY (name, data_type);
ALTER TABLE "collorg.actor".function DROP COLUMN inst_group;
