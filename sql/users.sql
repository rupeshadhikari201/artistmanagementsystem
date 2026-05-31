create table if not exists users (
    id serial primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null,
    password varchar(500) not null,
    phone varchar(20) not null,
    dob date,
    gender char(1) check (gender in ('m', 'f', 'o')),
    address varchar(255),
    role varchar(20) not null default 'artist' check (
        role in (
            'super_admin',
            'artist_manager',
            'artist'
        )
    ),
    created_at timestamp not null default now(),
    updated_at timestamp not null default now(),
    constraint unique_user_email unique (email)
);