include defs.mk

test::
	make -C testbed test

debug_mark::

check::

clean::
	python ./setup.py clean

.PHONY:
build: MANIFEST.in ./setup.py
	python ./setup.py sdist bdist_wheel

install:
	sudo python ./setup.py install

uninstall:
	sudo pip uninstall testbed
