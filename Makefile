include standard_defs.mk

.PHONY: test
test::
	$(foreach module,$(SUBDEFS), make -C $(dir $(module)) Makefile test;)
