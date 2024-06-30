FROM python:3.12-slim-bookworm as builder
RUN pip install --upgrade poetry poetry-plugin-export
ADD poetry.lock /app/
ADD pyproject.toml /app/

WORKDIR "/app"
RUN poetry export > /app/requirements.txt


FROM python:3.12-slim-bookworm

ENV RBACKUP_PATH=/app/rbackup

COPY --from=builder /app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD rbackup /app/rbackup
ADD bin/* /usr/bin/

WORKDIR "/app"
ENTRYPOINT ["/usr/bin/rbackup"]
