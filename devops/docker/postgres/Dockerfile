FROM postgres:13-alpine

# Attention: This script is only run, when no database exists
COPY init.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init.sh
