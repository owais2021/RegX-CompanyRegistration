@echo off
echo Running Python script...
docker exec -d ckan-docker-ckan-dev-1 /bin/bash -c "export PYTHONUNBUFFERED=1 && cd /srv/app/src_extensions/ckanext-regx/ckanext/regx && python main.py > /proc/1/fd/1 2>/proc/1/fd/2"

echo Done!
pause
