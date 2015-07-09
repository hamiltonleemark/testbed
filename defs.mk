SUBDEFS:=$(wildcard */defs.mk)
$(foreach module,$(SUBDEFS),\
    $(eval SUBDIR:=$(dir $(module))$(eval include $(module))))

.PHONY: help
help::
	echo "pylint - run pylint on python files."
	echo "pyflakes - run pyflakes on python files."
	echo "pep8 - run pep8 on python files."

.PHONY: pyflakes
pyflakes::
	pyflakes $(PYTHON_FILES)


.PHONY: pylint
pylint::
	pylint -j 2 --reports=n \
	       --generated-members=objects,MultipleObjectsReturned,get_or_create \
           $(PYTHON_FILES)

.PHONY: pep8
pep8::
	pep8 $(PYTHON_FILES)

check: pylint pep8 pyflakes
