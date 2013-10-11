alter table "collorg.communication.blog".post add column expiration_date timestamp(0);
alter table "collorg.communication.blog".post add column important boolean default 'f';
alter table "collorg.communication.blog".post add column broadcast boolean default 'f';
