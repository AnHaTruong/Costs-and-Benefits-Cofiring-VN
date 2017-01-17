# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3

tables = tableA.txt tableB.txt tableC.txt tableD.txt table1.txt table5.txt table7.txt table8.txt table11.txt table12.txt

tests = job.test emission.test npv.test health.test lcoe.test farmerincome.test biomassrequired.test benefitaddup.test biomasscost.test

all: $(tables)

%.test: %.py parameters.py
	$(PYTHON) $< > $@
	#TODO: actually test if the file is empty or not and cry if error
	@echo "Tests pass when the file is empty:"
	@cat $@ 

%.txt: %.py parameters.py
	$(PYTHON) $< > $@

.PHONY: test clean cleaner

test: $(tests)

clean:
	rm -f $(tables)
	rm -f $(tests)

cleaner: clean
	rm -f __pycache__/*.pyc *.pyc
