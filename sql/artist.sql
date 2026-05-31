create table if not exists artist (
    id serial primary key,
    name varchar(255) not null,
    dob date,
    gender char(1) check (gender in ('m', 'f', 'o')),
    address varchar(255),
    first_release_year integer check (
        first_release_year >= 1900
        and first_release_year <= extract(
            year
            from now()
        )
    ),
    no_of_albums_released integer not null default 0 check (no_of_albums_released >= 0),
    created_at timestamp not null default now(),
    updated_at timestamp not null default now()
)