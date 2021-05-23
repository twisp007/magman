CREATE TABLE "mlinks" (
  "infohash" VARCHAR PRIMARY KEY NOT NULL,
  "magnetLink" VARCHAR,
  "title" VARCHAR,
  "uploader" VARCHAR,
  "size" NUMBER,
  "seeds" NUMBER,
  "peers" NUMBER,
  "verified" BOOL DEFAULT 0,
  "source" VARCHAR,
  'retrieved' BOOL DEFAULT 0
);
