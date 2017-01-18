# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3

#tests = $(addsuffix .test, $(basename ./*.py))

tables = $(patsubst %.py,%.txt,$(wildcard table*.py))
diffs  = $(patsubst %.py,%.diff,$(wildcard table*.py))

tests = $(patsubst %.py,%.test,$(wildcard *.py))


all: $(tables)

%.diff: %.txt tables.tocompare/%.txt
	@diff $^  > $@
	@if [ -s $@ ]; then exit 1; fi;

%.test: %.py parameters.py
	$(PYTHON) $< > $@
	#TODO: actually test if the file is empty or not and cry if error
	@echo "Tests pass when the file is empty:"
	@cat $@ 

%.txt: %.py parameters.py
	$(PYTHON) $< > $@

.PHONY: test doctests regtests clean cleaner

test: doctests regtests

doctests: $(tests)

regtests: $(diffs)
	@cat $^

regtests-reset: $(tables)
	cp $^ tables.tocompare

clean:
	rm -f $(tables)
	rm -f $(tests)
	rm -f $(diffs)

cleaner: clean
	rm -f __pycache__/*.pyc *.pyc
