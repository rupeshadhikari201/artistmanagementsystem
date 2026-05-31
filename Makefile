DB_NAME=ams
DB_USER=postgres
DB_PORT=5432
DB_PASSWORD=root
DB_HOST=localhost

SQL_DIR=./sql

SQL_FILES=\
	$(SQL_DIR)/artist.sql \
	$(SQL_DIR)/music.sql \
	$(SQL_DIR)/users.sql \
	$(SQL_DIR)/audit_log.sql 

db-migrate:
	@echo "Starting Migration."
	@for file in $(SQL_FILES); do \
		echo "File Name $$file.."; \
		PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST) -U $(DB_USER) -p $(DB_PORT) -d $(DB_NAME) -f $$file; \
	done
	@echo "Migration Ended."