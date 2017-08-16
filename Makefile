# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016, 2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3

tables = tables_manuscript.txt

figurespyfiles = $(wildcard figure*.py)
figures = $(patsubst %.py,%.png,$(figurespyfiles))

all: $(tables) $(figures)

%.py: %_generator.py
	$(PYTHON) $< > $@

parameters.py: strawdata.py

%.txt: %.py parameters.py
	$(PYTHON) $< > $@

%.png: %.py
	$(PYTHON) $< > $@

classes.dot packages.dot:
	pyreverse3 *py

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
	cp *py $(distName)
	cp -r _regtest_outputs $(distName)
	cp -r Data $(distName)
	zip -r $(distName).zip $(distName)
	rm -rf $(distName)

test: cleaner
	py.test-3 --doctest-modules

regtest-reset:
	py.test-3 --regtest-reset

lint:
	pylint3 *py

docstyle:
	# Ignored messages:
	# D102: Missing docstring in public method             too many positives
	# D105: Missing docstring in magic method              why does it need a docstring ?
	# D203: 1 blank line required before class docstring   bug in the tool
	pydocstyle --ignore=D102,D105,D203 *py

codestyle:
	pycodestyle

clean:
	rm -f $(tables)
	rm -f $(figures)

cleaner: clean .git/hooks/pre-commit
	find . -type f -name '*.pyc' -delete
	rm -rf __pycache__
	rm -rf classes.dot packages.dot

