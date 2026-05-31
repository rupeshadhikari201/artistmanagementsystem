create table if not exists audit_log (
    id bigserial primary key,
    user_id integer references users (id) on delete set null,
    user_email varchar(255),
    user_role varchar(20),
    action varchar(10) not null check (
        action in ('create', 'update', 'delete')
    ),
    table_name varchar(100) not null,
    record_id integer not null,
    created_at timestamp not null default now()
)