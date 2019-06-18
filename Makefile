# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3
PYTEST = python3 -m pytest
PYLINT = pylint3
SOURCEDIRS = model manuscript1 lcoe

tables = tables_manuscript.txt feasibility.txt

figures = figure2.png figure3.png LCOE1.png LCOE1a.png LCOE2.png LCOE3.png

all: $(tables) $(figures)
 
feasibility.txt: manuscript1/feasibility.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.feasibility > $@

figure2.png: manuscript1/figure2.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.figure2 > $@

figure3.png: manuscript1/figure3.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.figure3 > $@

LCOE1.png LCOE1a.png LCOE2.png LCOE3.png: lcoe/figures.py
	$(PYTHON) -m lcoe.figures

tables_manuscript.txt: manuscript1/tables_manuscript.py manuscript1/parameters.py
	$(PYTHON) -m manuscript1.tables_manuscript > $@


classes.dot packages.dot:
	pyreverse3 *py */*.py

.git/hooks/pre-commit: pre-commit
	cp $^ $@

.PHONY:  archive test regtest-reset lint docstyle codestyle clean cleaner

distName:=CofiringEconomics-$(shell date --iso-8601)
dirs=$(distName) $(distName)/data $(distName)/data/VNM_adm_shp $(distName)/tables.tocompare

archive:
	-@rm -rf $(distName) 2>/dev/null
	mkdir $(dirs)
	cp Makefile $(distName)
	cp README $(distName)
	cp *py */*.py $(distName)
	cp -r _regtest_outputs $(distName)
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
	rm -f $(tables)
	rm -f $(figures)

cleaner: clean .git/hooks/pre-commit
	find . -type f -name '*.pyc' -delete
	rm -rf __pycache__
	rm -rf classes.dot packages.dot
	rm -rf .coverage coverage.xml htmlcov

