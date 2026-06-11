create table student(name varchar(30),age int,gender varchar(1),marks int,result varchar(5));

desc student;

insert into student values("Anjith",20,"M",850,"Pass");
insert into student values
("Mohith",19,"M",700,"Fail"),
("Teja",20,"M",900,"Pass");

desc student;
select * from student;

drop table student;

create table emp (f_name varchar(15), l_name varchar(15), age int,salary int);

desc emp;

insert into emp values
("A","B",25,50000),
("B","C",35,80000),
("C","D",26,36000),
("D","E",54,70000);

select * from emp;

alter table emp rename column f_name to first_name;
alter table emp change l_name last_name varchar(15);

select * from emp;



update emp set salary=60000 where age=54;

SET SQL_SAFE_UPDATES = 0;

alter table emp modify column first_name varchar(15) NOT NULL;

desc emp;
select * from emp;

insert into emp values
("","Z",56,14000);

insert into emp values
(null,"Z",56,52000);

delete from emp
where first_name = "";


ALTER TABLE emp
ADD COLUMN emp_id INT;

alter table emp drop column emp_id;
UPDATE emp 
SET emp_id = CASE first_name
    WHEN 'A' THEN 1
    WHEN 'B' THEN 2
    WHEN 'C' THEN 3
    WHEN 'D' THEN 4
END
WHERE first_name IN ('A', 'B', 'C', 'D');

select	first_name as fn,last_name as ln from emp;


select * from emp;

UPDATE emp 
SET first_name = CASE first_name
    WHEN 'A' THEN 'Alex'
    WHEN 'B' THEN 'Ben'
    WHEN 'C' THEN 'Charlie'
    WHEN 'D' THEN 'David'
END
WHERE first_name IN ('A', 'B', 'C', 'D');

select * from emp where first_name like '%h__l%';

create table empinfo(first varchar(15),last varchar(15), id int primary key,age int,city varchar(5),state varchar(5));
insert into empinfo values
("John","Jones",99980,45,"MPL","AP"),
("Mary","Jones",99982,25,"MPL","AP"),
("Eric","Edwards",88232,32,"NLR","AP"),
("Mary Ann","Edwards",88233,32,"BGE","KN"),
("Giger","Howell",98002,42,"BGE","KN"),
("Sebastian","Smith",92001,23,"CN","TN"),
("Gus","Gray",22322,35,"HYD","TS"),
("Mary Ann","May",32326,52,"HYD","TS");

select * from empinfo;

select * from empinfo where state = "TS";
select * from empinfo where age<=35 or age>=40;
select count(*) from empinfo;
select id from empinfo where city="MPL";

select count(*) from empinfo where state ="AP";

select count(age) from empinfo where state ="AP";

insert into empinfo values
(null,null,11111,null,"MPL","AP");

create database student;
use student;

create table emp(
first_name varchar(20),
last_name varchar(20),
designation varchar(20),
age int,
salary float);

insert into emp values
('Kiran','Ji','Secretary',24,19500.00);

insert into emp values
('Vignesh','Ji','Programmer',25,45300.00),
("Teja","Vardhan","Develper",20,50000.00),
("Anjith Kumar","Bathala",null,22,70000.00);

insert into emp values
('Mahesh','Bob','Hero',45,98765.35);

select * from emp;

select first_name from emp where salary>=50000;

alter table emp change salary salary decimal(10,2);
update emp set designation="IT Officer" where age=22;
desc emp;
alter table emp add column slno int auto_increment key;
alter table emp drop column slno;

update emp set age=age+1 where first_name="Teja";

alter table emp change desigation designation varchar(40);

update emp set designation="Administrative Assistant" where designation="Secretary";

update emp set last_name="Hero" where first_name="Mahesh";

update emp set salary=salary+3500 where salary<30000;

update emp set salary=salary+4500 where salary>=33500;

commit;

insert into emp values
('Mahesh','Bob','Hero',45,33500);

delete from emp where last_name="Bob";
