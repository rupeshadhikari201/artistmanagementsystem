create table if not exists music (
    id serial primary key,
    artist_id integer not null,
    title varchar(255) not null,
    album_name varchar(255),
    genre varchar(20) check (
        genre in (
            'rnb',
            'country',
            'classic',
            'rock',
            'jazz'
        )
    ),
    created_at timestamp not null default now(),
    updated_at timestamp not null default now(),
    constraint fk_music_artist foreign key (artist_id) references artist (id) on delete cascade on update cascade
);