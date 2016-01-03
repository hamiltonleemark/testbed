include defs.mk

test::
	make -C testbed test

debug_mark::

check::

clean::
	python ./setup.py clean
	rm -rf dist build testbed.egg-info

.PHONY:
build: MANIFEST.in ./setup.py 
	python ./setup.py build sdist bdist_wheel

install: build
	sudo pip install --upgrade dist/*.tar.gz

uninstall:
	sudo pip uninstall testbed
