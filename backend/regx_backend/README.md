# Usage 

Start the backend with: python manage.py runserver

To get Python working with Postgres, you will need to install the “psycopg2” module. However, you must first have pg_config installed on your OS:

[root@pga /]# pg_config

bash: pg_config: command not found

[root@pga /]# export PATH=/usr/pgsql-12/bin/:${PATH}

[root@pga /]# which pg_config

/usr/pgsql-12/bin/pg_config

# ToDo Database anbindung
Wichtige dfaten wie Password verschlüsseln
Testen über nightingnale

# PgBounder führ Verbindungspool?
# Welche Daten werden oft abgefragt? --> evtl. caching?
