use majormatch_db;

load data local infile 'majors.csv'
into table programs 
fields terminated by ',' 
enclosed by ''''
lines terminated by '\n'
(`name`, is_major, is_minor, `url`);