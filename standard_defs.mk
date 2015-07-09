SUBDEFS:=$(wildcard */defs.mk)
$(foreach module,$(SUBDEFS),\
    $(eval SUBDIR:=$(dir $(module))$(eval include $(module))))

.PHONY: help
help::
	echo "pylint - run pylint on python files."

.PHONY: pylint
pylint::
	pylint -j 2 --reports=n \
	       --generated-members=objects,MultipleObjectsReturned \
           $(PYTHON_FILES)

.PHONY: pep8
pep8::
	pep8 $(PYTHON_FILES)

check: pylint pep8
