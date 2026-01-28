drop table if exists blog_user;
drop table if exists newsletter_subscriber;
drop table if exists post;

create table if not exists blog_user (
    id serial primary key,
    username text unique not null,
    password text not null
);

create table if not exists newsletter_subscriber (
    email text unique not null
);

create table if not exists post (
    id serial primary key,
    author integer references blog_user,
    created timestamp not null default current_timestamp,
    title text not null,
    body text not null
);
