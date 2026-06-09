use college;
create table Customer(customer_id Int primary key not null,customer_name varchar(25),Place varchar(20),ddddDelivary_status varchar(20));
insert into Customer values (1,"Tejaswa","Madanapalle","Y");
insert into Customer values (2,"Rahul","Chennai","N");
insert into Customer values (3,"Hemanth","Madanapalle","Y");
insert into Customer values (4,"Ganesh","Angallu","Y");
insert into Customer values (5,"Santhosh","Hyderabad","N");
select * from Customer;
insert into Customer values 
(6,"Vikhyath","Vellore","Y"),
(7,"Ramesh","Chittor","Y");
create table Orders(Order_id int primary key not null, Delivary_status varchar(20),customer_id int, foreign key (customer_id) references Customer(customer_id));
insert into Orders values (101,"Y",1);
insert into Orders values (102,"N",2);
insert into Orders values (103,"Y",3);
insert into Orders values (104,"Y",4);
insert into Orders values (105,"N",5);
insert into Orders values (106,"Y",6);
insert into Orders values (107,"Y",7);
select * from Orders;