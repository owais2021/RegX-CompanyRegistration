@echo off
echo Running Python script...
docker exec ckan-docker-ckan-dev-1 /bin/bash -c "cd /srv/app/src_extensions/ckanext-regx/ckanext/regx && python main.py"
echo Done!
pause
