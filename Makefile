# Installs poetry
poetry:
	pip3 install poetry poetry-plugin-export --break-system-packages

install:
	poetry install --no-root

test:
	PYTHONPATH=. poetry run pytest -s .

bin/rclone:
	rm -rf /tmp/rclone
	mkdir -p /tmp/rclone
	wget https://downloads.rclone.org/v1.67.0/rclone-v1.67.0-linux-amd64.zip -O /tmp/rclone/rclone.zip
	cd /tmp/rclone && unzip rclone.zip
	mv /tmp/rclone/*/rclone ./bin/rclone
