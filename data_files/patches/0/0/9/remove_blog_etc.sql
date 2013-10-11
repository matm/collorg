ALTER TABLE "collorg.core".oid_table DROP COLUMN removed;

SET search_path = "collorg.core";
DELETE FROM base_table where cog_fqtn like 'collorg.communication%' ;
DELETE FROM oid_table where cog_oid NOT IN ( select cog_oid from base_table);
SET search_path = "collorg.application";
DELETE FROM a_action_task where action in (SELECT cog_oid FROM action WHERE data_type like 'collorg.communication%');
DELETE FROM action where data_type like 'collorg.communication%' ;
SET search_path = "collorg.core";
DELETE FROM field where fqfn like 'collorg.web.forum%';
DELETE FROM data_type where fqtn like 'collorg.web.forum%';
DROP TABLE "collorg.web".forum;
DELETE FROM field where fqfn like 'collorg.communication%';
DELETE FROM data_type where fqtn like 'collorg.communication%';
DROP TABLE "collorg.communication".article;
DROP TABLE "collorg.communication".blog;
DROP TABLE "collorg.communication".a_topic_data;
DROP TABLE "collorg.communication".topic CASCADE;
DELETE FROM oid_table WHERE cog_oid NOT IN (SELECT cog_oid FROM base_table);
SET search_path = "collorg.application";
DELETE FROM a_action_task where action = (SELECT cog_oid FROM action WHERE name = 'w3edit_link' AND data_type = 'collorg.communication.blog.post');
DELETE FROM action WHERE name = 'w3edit_link' AND data_type = 'collorg.communication.blog.post';

SET search_path = "collorg.access", "collorg.core";
DROP TABLE a_access_group;
DELETE FROM field WHERE fqfn like 'collorg.access.a_access_group%';
DELETE FROM data_type WHERE fqtn like 'collorg.access.a_access_group%';
