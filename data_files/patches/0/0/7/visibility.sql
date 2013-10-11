CREATE TABLE "collorg.access".visibility (
visibility STRING NOT NULL
   CHECK (visibility IN ('private', 'protected', 'public'))
);
