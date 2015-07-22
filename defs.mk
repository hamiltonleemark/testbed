SUBDEFS:=$(wildcard */defs.mk)
SUBMODULES:=$(foreach module,$(SUBDEFS),$(dir $(module)))

.PHONY: subdirs $(SUBMODULES)
$(SUBMODULES):
	make -C $@ $(MAKECMDGOALS)

subdirs: $(SUBMODULES)

PYTHONPATH+=/home/mark/ws/personal/testbed


.PHONY: help
help::
	echo "pylint - run pylint on python files."
	echo "pyflakes - run pyflakes on python files."
	echo "pep8 - run pep8 on python files."

.PHONY: pyflakes
%.pyflakes:: 
	pyflakes $*

pyflakes:: $(addsuffix .pyflakes,$(PYTHON_FILES))


.PHONY: pylint
%.pylint::
	pylint --reports=n --disable=I0011 \
          --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
	  --generated-members=objects,MultipleObjectsReturned,get_or_create $*

pylint:: $(addsuffix .pylint,$(PYTHON_FILES))


%.pep8:
	pep8 $*

.PHONY: pep8
pep8:: $(addsuffix .pep8,$(PYTHON_FILES))

check:: pep8 pylint pyflakes subdirs
