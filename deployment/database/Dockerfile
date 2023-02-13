FROM postgres

COPY sql_init.sql /

ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB docker

CMD ["/usr/bin/psql", "-U", "docker", "-d", "docker", "-a", "-f", "/sql_script.sql"]