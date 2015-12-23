include defs.mk

test::
	./testdbsite/manage.py test -v 2
	make -C testdbsite test
debug_mark::

check::

clean::
	rm -rf build dist testbed.egg-info
