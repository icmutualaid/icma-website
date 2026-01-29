delete from post;
delete from blog_user;
delete from newsletter_subscriber;

-- Reset serial sequences so tests get deterministic IDs
alter sequence if exists blog_user_id_seq restart with 1;
alter sequence if exists post_id_seq restart with 1;

insert into blog_user (username, password)
values
    ('TEST', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
    ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

insert into newsletter_subscriber (email)
values
    ('test email');

insert into post (title, body, author, created)
values
    ('test title', E'test\nbody', (select id from blog_user where username='TEST'), '2018-01-01 00:00:00');
