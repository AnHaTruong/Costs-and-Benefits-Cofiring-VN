# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3
PYTEST = python3 -m pytest
PYLINT = pylint3
SOURCEDIRS = model manuscript1 lcoe tests

figures-lcoe =  LCOE-4tech-3years-catalogue.png LCOE-4tech-3years-IEAfuelcosts.png\
                LCOE-4tech-2020-catalogueextremes.png LCOE-4tech-2050-catalogueextremes.png\
                LCOE-asDEA2019.png
figures-manuscript1 = figure_emissions.svg figure_benefits.svg figure_economics.svg
tables-manuscript1 = tables_manuscript.txt table_jobs.txt table_feasibility.txt table_emissionreduction.txt table_parameters.txt table_parameters_emission_factors.txt

all: $(tables) $(figures-lcoe) $(figures-manuscript1) $(tables-manuscript1)
 
feasibility.txt: manuscript1/feasibility.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.feasibility > $@

figure_%.svg: manuscript1/figure_%.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.figure_$* > $@

$(figures-lcoe): lcoe/figures.py
	$(PYTHON) -m lcoe.figures

table_%.txt: manuscript1/table_%.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.table_$* > $@

tables_manuscript.txt: manuscript1/tables_manuscript.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.tables_manuscript > $@

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
	$(PYTEST) --doctest-modules

coverage: coverage.xml
	python3.5-coverage html
	see htmlcov/index.html

coverage.xml:
	$(PYTEST) --doctest-modules --cov=. --cov-report term-missing --cov-report xml

codacy-update: coverage.xml
	export CODACY_PROJECT_TOKEN=e69e0e5c845f4e2dbc1c13fbaa35aeab; python-codacy-coverage -r coverage.xml

regtest-reset:
	$(PYTEST) --regtest-reset

lint:
	$(PYLINT) */*.py

docstyle:
	pydocstyle $(SOURCEDIRS)

codestyle:
	pycodestyle


clean:
	rm -f $(figures-lcoe) $(figures-manuscript1) $(tables-manuscript1)

cleaner: clean
	find . -type f -name '*.pyc' -delete
	rm -rf __pycache__ .pytest_cache
	rm -rf classes.dot packages.dot
	rm -rf .coverage coverage.xml htmlcov

