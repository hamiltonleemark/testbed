*******
Release
*******

These are the steps for releasing testbed.

  1. make sdist

To test the distribution

  1. virtualenv --no-site-package pip_test_env
  2. . pip_test_env/bin/activate
  3. pip install -e .
