use majormatch_db;

-- drop in reverse order
drop table if exists form_data;
drop table if exists major_pairs;
drop table if exists programs;
drop table if exists courses;

create table courses (
    cid int not null AUTO_INCREMENT,
    dept varchar(10),
    cnum varchar(10),
    `name` varchar(100),
    units float(2),
    max_enroll int,
    prereq varchar(100),
    instruct varchar(30),
    dr varchar(100),
    sem_offered varchar(30),
    year_offered varchar(30),
    primary key (cid)
)
ENGINE = InnoDB;

create table programs (
    dept_id int not null AUTO_INCREMENT,
    `name` varchar(80),
    is_major tinyint(1),
    is_minor tinyint(1),
    `url` varchar(200),
    primary key (dept_id)
)
ENGINE = InnoDB;

create table major_pairs (
    dept_id int,
    cid int,
    foreign key (dept_id) references programs(dept_id)
        on delete restrict
        on update cascade,
    foreign key (cid) references courses(cid)
        on delete restrict
        on update cascade
)
ENGINE = InnoDB;

create table form_data (
    dept varchar(10),
    cnum varchar(10),
    cid int,
    foreign key (cid) references courses(cid)
        on delete restrict
        on update cascade
)
ENGINE = InnoDB;

