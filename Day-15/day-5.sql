use college;
create database fun;
use fun;
create table players
(
player_id int,
player_name varchar(20),
country varchar(20),
goals int
);


insert into players values(1,'Ronaldo','Portugal',100);

insert into players values(2,'Messi','Argentina',90);

insert into players values(3,'Neymar','Brazil',90);

insert into players values(4,'Sunil','India',110);

insert into players values(5,'Jagadish','USA',10);

insert into players values(6,'Peddi','Global star',150);

select * from players;

delete from players;

TRUNCATE TABLE players;

select * from players;

select * from players where goals > 100;

delimiter &&
create procedure top_players()
begin
select player_name,country,goals from players where goals>100;
end&&
delimiter ; 

call top_players();

Q1. Create a procedure which returns the top players based on goals

delimiter //
create procedure top_players_sort(in num int)
begin
select player_name,player_id,country from players where goals>120;
end //
delimiter ;

delimiter //
create procedure top_players_cos5(in var varchar(20),out total_players int)
begin
select count(*) from players where country = var into total_players;
end//
delimiter;
drop procedure top_players_cos1;
call top_players_cos('India',@total_count);
select @total_count as top_players_cos5;


delimiter //
create procedure update_players (in num int, in player varchar(25))
begin
update players set goals =num where player_name=player;
end //
delimiter;

call update_players(300,'Ronaldo');

select * from players;




call top_players_sort(1);

select * from players where order by goals desc 
Q2. using update
create procedure top_players_list(in num int)


delimiter //
