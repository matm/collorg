update "collorg.application".action set in_header = 't', icon = 'users_list.svg', label='members list' where name = 'w3list_members';
update "collorg.application".action set in_header = 't', icon = 'edit.svg', label='Edit' where name = 'w3edit' and data_type = 'collorg.communication.blog.post';
update "collorg.application".action set in_header = 't', icon = 'compose.svg', label='New post' where name = 'w3new_post' and data_type = 'collorg.core.base_table';
