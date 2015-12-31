include defs.mk

test::
	make -C testbed test

debug_mark::

check::

clean::
	rm -rf build dist testbed.egg-info

.PHONY:
build: MANIFEST.in ./setup.py
	python ./setup.py sdist bdist_wheel
