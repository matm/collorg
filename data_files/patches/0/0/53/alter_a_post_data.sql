alter table "collorg.communication.blog".a_post_data add column who c_oid;
alter table "collorg.communication.blog".a_post_data add constraint who_fk foreign key(who) references "collorg.actor"."user"(cog_oid);
alter table "collorg.communication.blog".a_post_data add column "when" timestamp(0) default ('now'::text)::timestamp(0) with time zone;
alter table "collorg.communication.blog".a_post_data add column private_reference boolean default 'f';
