rbackup
=======

Simple backup upload & rotation cli commands.

### Perform a rotation & upload

```bash
python3 -m rbackup -m 4 -r '{"path": "/tmp/test-del"}' ./README.md ""
```


### Keep only last 4 versions in /tmp/test-del directory

```bash
python3 -m rbackup.rotate -m 4 -r '{"path": "/tmp/test-del"}'
```

### Keep only last 2 files on remote S3 bucket

- Only last 2 files: `-m 2`
- Only matching pattern: `.*\.csv`

```bash
python3 -m rbackup.rotate -m 2 --remote-type s3 -r '{"endpoint": "http://127.0.0.1:9000", "access_key_id": "anarchism", "secret_key_id": "anarchism", "bucket_name": "test", "base_dir": "backups"}' -p '.*\.csv'
```

### Complete example with Min.io

```bash
# at first upload, do it multiple times
python3 -m rbackup.upload --remote-type s3 -r '{"endpoint": "http://127.0.0.1:9000", "access_key_id": "anarchism", "secret_key_id": "anarchism", "bucket_name": "test", "base_dir": "backups"}' ./README.md ""

# then rotate files
python3 -m rbackup.rotate -m 2 --remote-type s3 -r '{"endpoint": "http://127.0.0.1:9000", "access_key_id": "anarchism", "secret_key_id": "anarchism", "bucket_name": "test", "base_dir": "backups"}' -p 'backup-(.*)
```

### Example with End-To-End (E2E) encrypted S3 remote (using rclone)

```bash
python3 -m rbackup --remote-type s3crypto -r '{"endpoint": "http://127.0.0.1:9000", "enc_password": "test123test123", "enc_salt_password": "testtesttesttesttest", "base_dir": "", "access_key_id": "anarchism", "secret_key": "anarchism", "bucket_name": "test"}' -m 4 ./README.md --pattern '(.*)\.md'
```
