-- sqlite3 db/lettres.dev.sqlite < db/utils/remove_unique_constraint_label.sql

DROP INDEX IF EXISTS person_label_uindex ;
DROP INDEX IF EXISTS placename_label_uindex;
