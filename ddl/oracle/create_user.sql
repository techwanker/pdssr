set echo on
create user &&username identified by &password;
alter user &&username quota unlimited on users;
grant connect to &&username;
grant create table to &&username;
alter user &&username default tablespace users;
grant create sequence to &&username;
grant select any table to &&username;
exit;
