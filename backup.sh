#!/bin/bash

echo "backing up docker volumes..."

docker run --rm --volumes-from paperless_consumer_1 -v ~/backup/volumes:/backup ubuntu bash -c "cd /usr/src/paperless && tar cvf /backup/paperless.tar ."

echo "paperless backup complete"

docker run --rm --volumes-from firefly_app -v ~/backup/volumes:/backup ubuntu bash -c "cd /var/www/firefly-iii/storage && tar cvf /backup/firefly_app.tar ."

echo "firefly_app backup complete"

docker run --rm --volumes-from firefly_db -v ~/backup/volumes:/backup ubuntu bash -c "cd /var/lib/postgresql/data && tar cvf /backup/firefly_db.tar ."

echo "firefly_db backup complete"
