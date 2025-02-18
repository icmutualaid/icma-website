drop table blog_user;
drop table newsletter_subscriber;
drop table post;

create table blog_user (
    id serial primary key,
    username text unique not null,
    password text not null
);

create table newsletter_subscriber (
    email text unique not null
);

create table post (
    id serial primary key,
    author integer references blog_user,
    created timestamp not null default current_timestamp,
    title text not null,
    body text not null
);
