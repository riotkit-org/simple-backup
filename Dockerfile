FROM python:3.12-slim-bookworm as builder
RUN pip install --upgrade poetry poetry-plugin-export
RUN apt-get update && apt-get install -y make wget unzip
ADD poetry.lock /app/
ADD pyproject.toml /app/
ADD Makefile /app
RUN mkdir /app/bin

WORKDIR "/app"
RUN poetry export > /app/requirements.txt
RUN make bin/rclone


# ============
# Target image
# ============
FROM python:3.12-slim-bookworm

ENV RBACKUP_PATH=/app/rbackup

COPY --from=builder /app/requirements.txt /app/requirements.txt
COPY --from=builder /app/bin/rclone /usr/bin/rclone
RUN pip install -r /app/requirements.txt

ADD rbackup /app/rbackup
ADD bin/* /usr/bin/

WORKDIR "/app"
ENTRYPOINT ["/usr/bin/rbackup"]
