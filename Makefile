# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

tables = tableA.txt tableB.txt tableC.txt tableD.txt table7.txt table8.txt

all: $(tables)

%.txt: %.py parameters.py
	python $< > $@


.PHONY: test clean cleaner

test: job.txt emission.txt npv.txt health.txt LCOE.txt farmerincome.txt
	@echo "Tests pass when the files are empty:"
	cat $^

clean:
	rm -f $(tables)
	rm -f job.txt emission.txt npv.txt health.txt LCOE.txt farmerincome.txt

cleaner: clean
	rm -f __pycache__/*.pyc *.pyc
