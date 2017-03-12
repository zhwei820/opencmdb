import MySQLdb
from skylark import Database, Model, Field
from django.conf import settings as _options

Database.set_dbapi(MySQLdb)
Database.config(host=_options.DATABASES['default']['HOST'], user=_options.DATABASES['default']['USER'],
                  passwd=_options.DATABASES['default']['PASSWORD'], port=int(_options.DATABASES['default']['PORT']),
                  db=_options.DATABASES['default']['NAME'], charset='utf8')
