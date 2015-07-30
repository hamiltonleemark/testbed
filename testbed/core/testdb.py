"""
Common content for database setup.
"""
import sys
import os
import testbed.settings
import django

""" When True the django database is initialized. """
def init(location="default"):
    """ Initialize database. 
    @param log_dir Directory for storing log information.
    @param logical name of database to setup.
    """

    print "MARK: path", sys.path
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsite.settings")
    sys.path.append(testbed.settings.TEST_DBSITE_DIR)
    import dbsite.settings
    from django.conf import settings
    django.setup()
