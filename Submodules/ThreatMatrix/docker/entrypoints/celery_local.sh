#!/bin/bash

until cd /opt/deploy/threat_matrix
do
    echo "Waiting for server volume..."
done

ARGUMENTS="-A threat_matrix.celery worker -n worker_local --uid www-data --time-limit=10000 --gid www-data --pidfile= -Ofair -Q local,broadcast,config -E --without-gossip"
if [[ $DEBUG == "True" ]] && [[ $DJANGO_TEST_SERVER == "True" ]];
then
    echo "Running celery with autoreload"
    python3 manage.py celery_reload -c "$ARGUMENTS"
else
  /usr/local/bin/celery $ARGUMENTS
fi