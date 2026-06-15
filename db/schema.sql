create database `movies_db`;
use `movies_db`;

create table `movie` (
`movie_id` int primary key auto_increment,
`title` varchar(255) unique not null,
`release_year` year,
`duration` smallint,
`budget` decimal(15,2),
`box_office` decimal(15,2)
);

create table `language` (
`language_id` int primary key auto_increment,
`name` varchar(100) unique not null
);

create table `country` (
`country_id` int primary key auto_increment,
`name` varchar(100) unique not null
);

create table `genre` (
`genre_id` int primary key auto_increment,
`name` varchar(100) unique not null
);

create table `director` (
`director_id` int primary key auto_increment,
`name` varchar(100) unique not null
);

create table `movie_languages` (
`language_id` int not null,
`movie_id` int not null,
primary key (`language_id`,`movie_id`),
constraint `fk_language_id`
foreign key (`language_id`) references `language` (`language_id`) on update cascade on delete cascade,
constraint `fk_ml_movie_id` 
foreign key (`movie_id`) references `movie` (`movie_id`) on update cascade on delete cascade
);

create table `movie_countries` (
`country_id` int not null,
`movie_id` int not null,
primary key (`country_id`,`movie_id`),
constraint `fk_country_id`
foreign key (`country_id`) references `country` (`country_id`) on update cascade on delete cascade,
constraint `fk_mc_movie_id` 
foreign key (`movie_id`) references `movie` (`movie_id`) on update cascade on delete cascade
);

create table `movie_genres` (
`genre_id` int not null,
`movie_id` int not null,
primary key (`genre_id`,`movie_id`),
constraint `fk_genre_id`
foreign key (`genre_id`) references `genre` (`genre_id`) on update cascade on delete cascade,
constraint `fk_mg_movie_id`
foreign key (`movie_id`) references `movie` (`movie_id`) on update cascade on delete cascade
);

create table `movie_directors` (
`director_id` int not null,
`movie_id` int not null,
primary key (`director_id`,`movie_id`),
constraint `fk_director_id`
foreign key (`director_id`) references `director` (`director_id`) on update cascade on delete cascade,
constraint `fk_md_movie_id`
foreign key (`movie_id`) references `movie` (`movie_id`) on update cascade on delete cascade
);
