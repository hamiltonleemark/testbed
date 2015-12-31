
sqllite_path = os.path.abspath(os.path.join(BASE_DIR, 'db.sqlite3'))

##
# Defines default SQL database
DEFAULT = {
    'ENGINE': 'django.db.backends.sqlite3',
    ##
    # This must point to the sqllite database built from
    # python ./manage.py init
    'NAME': sqllite_path,
}

# Assume if default is defined that this application has been installed
# and so is a release.
if "default" in DATABASES:
    DATABASES["local"] = DEFAULT

    DEBUG = False
    TEMPLATE_DEBUG = False
else:
    DATABASES["default"] = DEFAULT

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
