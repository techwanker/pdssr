.echo on 
/* http://stackoverflow.com/questions/9433250/foreign-key-constraint-doesnt-work *;
/* Assuming the library is compiled with foreign key constraints enabled, it must still be enabled by the application at runtime, using the PRAGMA foreign_keys command. For example:
sqlite> PRAGMA foreign_keys = ON;
*/

PRAGMA foreign_keys = ON;

CREATE TABLE artist(
  artistid    INTEGER PRIMARY KEY, 
  artistname  TEXT
);

CREATE TABLE track(
  trackid     INTEGER,
  trackname   TEXT, 
  trackartist INTEGER    REFERENCES artist(artistid)
);

insert into track (trackid, trackname, trackartist) 
values (1,'A',2);

select * from artist;

select * from track;

.save test.db

