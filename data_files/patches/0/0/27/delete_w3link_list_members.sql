delete from "collorg.application".a_action_task where action = ( select cog_oid from "collorg.application".action WHERE name = 'w3link_list_members' and data_type = 'collorg.group.group');
delete from "collorg.application".action WHERE name = 'w3link_list_members' and data_type = 'collorg.group.group';
