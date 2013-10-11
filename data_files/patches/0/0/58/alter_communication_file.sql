alter table "collorg.communication".file add column visibility string default 'protected' check ( visibility in ( 'private', 'protected', 'public' ));
