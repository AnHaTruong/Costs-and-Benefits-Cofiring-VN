# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3
PYTEST = python3 -m pytest
PYLINT = pylint3
SOURCEDIRS = . model WTPWTA

tables = tables_manuscript.txt

figurespyfiles = $(wildcard figure*.py)
figures = $(patsubst %.py,%.png,$(figurespyfiles))

all: $(tables) $(figures)
 
feasibility:
	$(PYTHON) -m WTPWTA.market


%.txt: %.py parameters.py
	$(PYTHON) $< > $@

%.png: %.py
	$(PYTHON) $< > $@

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
	$(PYLINT) *py
	$(PYLINT) */*.py

docstyle:
	pydocstyle $(SOURCEDIRS)

codestyle:
	pycodestyle $(SOURCEDIRS) tests

clean:
	rm -f $(tables)
	rm -f $(figures)

cleaner: clean .git/hooks/pre-commit
	find . -type f -name '*.pyc' -delete
	rm -rf __pycache__
	rm -rf classes.dot packages.dot
	rm -rf .coverage coverage.xml htmlcov

