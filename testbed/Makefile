ROOT=$(shell git rev-parse --show-toplevel)
include defs.mk
include $(ROOT)/defs.mk

test::
	./testdbsite/manage.py test -v 2
	make -C testdbsite test
