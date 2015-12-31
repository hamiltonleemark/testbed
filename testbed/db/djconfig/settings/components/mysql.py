print "MARK: WHAT"
MYSQL_CNF="/etc/testbed/mysql.cnf"
if os.path.exists(MYSQL_CNF):
    print "MARK: WHAT 2"
    DATABASES["default"] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testbed',
        'init_command': 'Set storage_engine=INNODB',
        'OPTIONS': {
            'read_default_file': MYSQL_CNF
            }
    }
