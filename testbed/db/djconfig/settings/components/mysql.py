MYSQL_CNF="/etc/testbed/mysql.cnf"
if os.path.exists(MYSQL_CNF):
    DATABASES["default"] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testbed',
        'init_command': 'Set storage_engine=INNODB',
        'OPTIONS': {
            'read_default_file': MYSQL_CNF
            }
    }
