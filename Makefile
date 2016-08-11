# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

tables = tableAA.txt tableB.txt tableC.txt tableD.txt table77.txt table88.txt

tests = job.test emission.test npv.test health.test LCOE.test farmerincome.test biomassrequired.test
 
all: $(tables)

%.test: %.py parameters.py
	python < > $@
	@echo "Tests pass when the file is empty:"
	cat $@


%.txt: %.py parameters.py
	python $< > $@


.PHONY: test clean cleaner

test: $(tests)
	@echo "Tests pass when the files are empty:"

clean:
	rm -f $(tables)
	rm -f $(tests)

cleaner: clean
	rm -f __pycache__/*.pyc *.pyc
