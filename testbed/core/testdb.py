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
    sys.path.append(os.path.join(testbed.settings.BASE_DIR, "dbsite"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsite.settings")
    from django.conf import settings
