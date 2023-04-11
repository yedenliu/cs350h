use majormatch_db;

-- Table has been created and admin row inserted

drop table if exists account;
create table account(
    userid int,
    user varchar(10) not null,
    hashedpw char(60),
    unique(user),
    index(user),
    primary key (userid)
);