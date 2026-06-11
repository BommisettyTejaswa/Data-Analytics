use college;
create table cust_info
(
customer_name varchar(50),
customerid varchar(20) primary key,
city varchar(20),
postalcode varchar(20),
country varchar(20)
);
create table order_info
(
order_id int primary key,
customer_id varchar(20) ,
employee_id int,
orderdate datetime,
shipper_id int
);
insert into cust_info values ("Ramesh","1","Chennai","000000","India");
insert into cust_info values ("Raju","2","Madanapalle","000000","India");
insert into cust_info values ("Rahul","3","Hyderbad","000000","India");
insert into cust_info values ("Ranjith","4","Mumbai","000000","India");
insert into cust_info values ("Hemanth","5","Delhi","000000","India");
insert into cust_info values ("Ram","6","Kolkata","000000","India");
insert into cust_info values ("Mohan","7","Vishakapatnam","000000","India");
insert into cust_info values ("Bunny","8","Chennai","000000","India");
alter table cust_info change customerid customer_id varchar(20); 
select * from cust_info;

insert into order_info values (1,"1",1,sysdate(),5000);
insert into order_info values (2,"2",1,sysdate(),5001);
insert into order_info values (3,"3",1,sysdate(),5002);
insert into order_info values (4,"4",1,sysdate(),5003);
insert into order_info values (5,"5",1,sysdate(),5004);
insert into order_info values (6,"6",1,sysdate(),5005);
insert into order_info values (7,"7",1,sysdate(),5006);
insert into order_info values (8,"8",1,sysdate(),5007);

select *from order_info;

select * from cust_info c inner join order_info o on c.customer_id=o.customer_id;

select * from cust_info c left join order_info o on c.customer_id=o.customer_id;

select * from cust_info c right join  order_info o on c.customer_id=o.customer_id;
-- outer join 
select * from cust_info c left join order_info o on c.customer_id=o.customer_id union 

select * from cust_info c right join  order_info o on c.customer_id=o.customer_id;

