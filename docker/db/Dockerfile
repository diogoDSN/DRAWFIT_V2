FROM postgres:14.6 as populate

ARG POSTGRES_PASSWORD
ARG BOT_PASSWORD

ENV PGDATA=/data

COPY src/database/initial_database.sql /

COPY src/database/init-db.sh /docker-entrypoint-initdb.d

# Replace exec "$@" with echo "skipping..."
# This ensures that when the script runs the postgres daemon won't start
RUN ["sed", "-i", "s/exec \"$@\"/echo \"skipping...\"/", "/usr/local/bin/docker-entrypoint.sh"]

RUN ["/usr/local/bin/docker-entrypoint.sh", "postgres"]

FROM postgres:14.6

COPY --from=populate /data $PGDATA

COPY src/database/pg_hba.conf $PGDATA
