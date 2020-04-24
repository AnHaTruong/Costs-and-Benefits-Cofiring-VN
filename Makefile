# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3
PYTEST = python3 -m pytest
# Parallel exectution on 2 jobs is the less slow, on my Intel Core i5-8250U CPU.
PYLINT = pylint3 -j 2
SOURCEDIRS = model manuscript1 sensitivity lcoe tests manuscript1/table manuscript1/figure
DOCTESTFILES := $(shell grep -l '>>>' */*.py */*/*.py)

figures-lcoe =  LCOE-4tech-3years-catalogue.png LCOE-4tech-3years-IEAfuelcosts.png\
                LCOE-4tech-2020-catalogueextremes.png LCOE-4tech-2050-catalogueextremes.png\
                LCOE-asDEA2019.png
figures-manuscript1 = figure_emissions.svg figure_economics.svg figure_cba.svg figure_sensitivity.svg 
tables-manuscript1 = tables_manuscript.txt\
                     table_jobs.txt\
                     table_emission_reduction.txt\
                     table_business_value.txt\
                     table_coal_saved.txt\
                     table_opex_details.txt\
                     table_parameter_systems.txt\
                     table_parameter_economics.txt\
                     table_parameter_emission_factors.txt\
                     table_uncertainty.txt\
                     table_sensitivity.txt

all: $(tables) $(figures-lcoe) $(figures-manuscript1) $(tables-manuscript1)

feasibility.txt: manuscript1/table/feasibility.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.table.feasibility > $@

$(figures-lcoe): lcoe/figures.py
	$(PYTHON) -m lcoe.figures

figure_%.svg: manuscript1/figure/%.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.figure.$* > $@

figure_%.svg: sensitivity/figure_%.py
	$(PYTHON) -m sensitivity.figure_$* > $@

table_%.txt: sensitivity/table_%.py
	$(PYTHON) -m sensitivity.table_$* > $@

table_%.txt: manuscript1/table/%.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.table.$* > $@

tables_manuscript.txt: manuscript1/table/manuscript.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.table.manuscript > $@

classes.dot packages.dot:
	pyreverse3 *py */*.py

.git/hooks/pre-commit: pre-commit
	cp $^ $@

install-pre-commit: .git/hooks/pre-commit

install:
	pip3 install -r requirements.txt

.PHONY:  archive test regtest-reset lint docstyle codestyle install install-pre-commit clean cleaner

distName:=CofiringEconomics-$(shell date --iso-8601)
dirs=$(distName) $(distName)/$(SOURCEDIRS) $(distName)/Data

archive:
	-@rm -rf $(distName) 2>/dev/null
	mkdir $(distName)
	cp stable-requirements.txt $(distName)
	cp requirements.txt $(distName)
	cp Makefile $(distName)
	cp pylintrc $(distName)
	cp setup.cfg $(distName)
	cp README.md $(distName)
	cp pre-commit $(distName)
	cp -r $(SOURCEDIRS) $(distName)
	cp -r Data $(distName)
	zip -r $(distName).zip $(distName)
	rm -rf $(distName)

test: cleaner
	$(PYTEST)

coverage: coverage.xml
	python3.7-coverage html
	see htmlcov/index.html

doctest:
	$(PYTHON) -m doctest $(DOCTESTFILES)

coverage.xml:
	$(PYTEST) --doctest-modules --cov=. --cov-report term-missing --cov-report xml

regtest-reset:
	$(PYTEST) --regtest-reset

lint:
	$(PYLINT) $(SOURCEDIRS)

docstyle:
	pydocstyle $(SOURCEDIRS)

black:
	black $(SOURCEDIRS)

codestyle:
	pycodestyle

clean:
	rm -f $(figures-lcoe) $(figures-manuscript1) $(tables-manuscript1) figure_benefits.svg

cleaner: clean
	find . -type f -name '*.pyc' -delete
	rm -rf __pycache__ .pytest_cache
	rm -rf classes.dot packages.dot
	rm -rf .coverage coverage.xml htmlcov

