.echo on 

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

