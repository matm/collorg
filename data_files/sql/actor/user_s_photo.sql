ALTER TABLE "collorg.actor"."user" ADD constraint user_photo_fkey FOREIGN KEY (photo) REFERENCES "collorg.communication".file(cog_oid);
