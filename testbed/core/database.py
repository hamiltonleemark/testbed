"""
Common content for database setup.
"""
import sys
import os
import testbed.settings
import django


def init():
    """ Initialize database.
    @param log_dir Directory for storing log information.
    @param logical name of database to setup.
    """

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djconfig.settings")
    sys.path.append(testbed.settings.TEST_DBSITE_DIR)
    # pylint: disable=W0612
    import djconfig.settings
    from django.conf import settings
    django.setup()
