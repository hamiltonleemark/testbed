include defs.mk

test::
	./testdbsite/manage.py test -v 2
	make -C testdbsite test

check::
