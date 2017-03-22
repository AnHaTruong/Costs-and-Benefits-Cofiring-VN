# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016, 2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3


tablepyfiles = $(wildcard table*.py)
tables = $(patsubst %.py,%.txt,$(tablepyfiles))
diffs  = $(patsubst %.py,%.diff,$(tablepyfiles))

figurespyfiles = $(wildcard figure*.py)
figures = $(patsubst %.py,%.eps,$(figurespyfiles))


allpyfiles  = $(wildcard *.py)
nontable  = $(filter-out $(tablepyfiles),$(allpyfiles))
nontablenonfigure  = $(filter-out $(figurespyfiles),$(nontable))
tests = Shape.test Investment.test init.test


all: $(tables)

%.py: %-generator.py
	$(PYTHON) $< > $@

parameters.py: strawdata.py

%.txt: %.py parameters.py
	$(PYTHON) $< > $@

%.diff: %.txt tables.tocompare/%.txt
	@diff $^  > $@
	@if [ -s $@ ]; then exit 1; fi;

%.test: %.py parameters.py
	$(PYTHON) $< > $@
	@#TODO: actually test if the file is empty or not and cry if error
	@#@echo "Tests pass when the file is empty:"
	@#@cat $@ 
	@if [ -s $@ ]; then cat $@ && exit 1; fi;


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
	find . -type f -name '*.pyc' -delete
	rm -f strawdata.py
	rm -rf __pycache__
