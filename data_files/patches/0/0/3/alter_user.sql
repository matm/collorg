--ALTER TABLE "collorg.actor"."user" ADD column biography wiki;
ALTER TABLE "collorg.actor"."user" ADD column photo c_oid;
ALTER TABLE "collorg.actor"."user" ADD column "url" url ;
ALTER TABLE "collorg.actor"."user" ADD constraint user_photo_fkey FOREIGN KEY (photo) REFERENCES "collorg.communication".file(cog_oid);
