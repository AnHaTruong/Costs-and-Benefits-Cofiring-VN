# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016, 2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3
PYTEST = py.test
PYLINT = pylint3

tables = tables_manuscript.txt

figurespyfiles = $(wildcard figure*.py)
figures = $(patsubst %.py,%.png,$(figurespyfiles))

all: $(tables) $(figures)

%.txt: %.py parameters.py
	$(PYTHON) $< > $@

%.png: %.py
	$(PYTHON) $< > $@

classes.dot packages.dot:
	pyreverse3 *py classes/*.py

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
	cp *py classes/*.py $(distName)
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
	$(PYLINT) classes/*.py

docstyle:
	# Ignored messages:
	# D102: Missing docstring in public method             too many positives
	# D105: Missing docstring in magic method              why does it need a docstring ?
	# D203: 1 blank line required before class docstring   bug in the tool
	# D213: Multi-line docstring summary should start at the second line
	pydocstyle --ignore=D102,D105,D107,D203,D213 *py classes/*.py

codestyle:
	# Ignore messages:
	# W503 line break before binary operator
	# W504: line break after binary operator
	# E265: Block comment should start with '# '
	pycodestyle --ignore=E265,W503,W504 *py classes/*.py

clean:
	rm -f $(tables)
	rm -f $(figures)

cleaner: clean .git/hooks/pre-commit
	find . -type f -name '*.pyc' -delete
	rm -rf __pycache__
	rm -rf classes.dot packages.dot
	rm -rf .coverage coverage.xml htmlcov

