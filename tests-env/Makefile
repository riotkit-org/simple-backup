test-minio-enc:
	cd .. && export PATH=$$PATH:./bin && ./bin/rbackup --remote-type s3crypto -r '{"endpoint": "http://127.0.0.1:9000", "enc_password": "test123test123", "enc_salt_password": "testtesttesttesttest", "base_dir": "", "access_key_id": "anarchism", "secret_key": "anarchism", "bucket_name": "test"}' -m 4 ./README.md --pattern '(.*)\.md'
