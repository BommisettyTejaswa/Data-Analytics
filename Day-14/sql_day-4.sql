use college;
select Datediff(sysdate(),'2026-09-09') as difference;
select date_format('2026-09-09','%d-%m-%y') as date;
select date_format('2026-09-09','%y-%m-%d') as date;
select date_format('2026-09-09','%d %M %y') as month;
select date_format('2026-09-09','%W') as week;
select day(sysdate()) as today;
select month(sysdate()) as month_;
select year(sysdate()) as year_;
select quarter(sysdate());
select adddate(sysdate(), interval  10 day) as days;
select adddate(sysdate(), interval  10 month) as months;
select adddate(sysdate(), interval  10 year) as years;
select adddate(sysdate(), interval  10 quarter) as quarters;

show tables;
select * from cust_info;

select count(*) from cust_info where customer_name like 'R%';

select count(*) from cust_info where customer_name regexp '[R%]'; 

select count(*) from cust_info where customer_name like 'R%' or customer_name like 'S%' or customer_name like 'T%';

select customer_name,count(*) from cust_info where customer_name regexp '[R-T]' group by customer_name;

select * from emp;

select first_name from emp where salary > (select avg(salary) from emp);

select avg(salary) from emp;

select first_name from emp where salary >(select salary from emp where first_name='Charlie');

select first_name from emp where salary=(select max(salary) from emp);

select salary from emp where salary<(select max(salary) from emp);

select first_name from emp where salary=(select max(salary) from emp where salary<(select max(salary) from emp));

select max(salary) from emp;

show tables;

 select * from data;
 
 create view data1 as 
 select * from  data where Gender='female'; 
 
 create view data2 as 
 select * from data where Gender='male';
 
 create view data3 as 
 select * from data where  Roll>1;
 
select * from data1;
 
select * from data2;
  
select * from data3;

create view data4 as 
select * from data;

select * from data4;


