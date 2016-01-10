
##
# Provides location of plain text file that defines the mysql connection
# information. The existance of the mysql configuration file implies that
# it will become default database.
MYSQL_CNF="/etc/testbed/mysql.cnf"

if os.path.exists(MYSQL_CNF):
    DATABASES["global"] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testbed',
        'init_command': 'Set storage_engine=INNODB',
        'OPTIONS': {
            'read_default_file': MYSQL_CNF
        }
    }
    DATABASES["default"] = DATABASES["global"]
