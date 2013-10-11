update "collorg.actor".function set name = 'Collorg actor' where name = 'ColOrg Actor';
delete from "collorg.access".role where function = (select cog_oid from "collorg.actor".function where name = 'Collorg actor');
update "collorg.application".action set in_header = 't', icon = 'compose.svg', label='New post' where name = 'w3new_post' and data_type = 'collorg.core.base_table';
