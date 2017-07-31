# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016, 2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

PYTHON = python3


tablepyfiles = $(wildcard table*.py)
tables = $(patsubst %.py,%.txt,$(tablepyfiles))

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

.precious: strawdata.py

.PHONY: test lint docstyle codestyle regtest_reset clean cleaner archive

distName:=CofiringEconomics-$(shell date --iso-8601)
dirs=$(distName) $(distName)/data $(distName)/data/VNM_adm_shp $(distName)/tables.tocompare $(distName)/natu

archive:
	-@rm -rf $(distName) 2>/dev/null
	mkdir $(dirs)
	cp Makefile $(distName)
	cp README $(distName)
	cp *py $(distName)
	cp -r tables.tocompare $(distName)
	cp -r Data $(distName)
	cp -r natu $(distName)
	zip -r $(distName).zip $(distName)
	rm -rf $(distName)

test: cleaner strawdata.py
	py.test-3 --doctest-modules --ignore=natu/

regtest_reset:
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
	pycodestyle --exclude=natu

clean:
	rm -f $(tables)
	rm -f $(figures)

cleaner: clean .git/hooks/pre-commit
	find . -type f -name '*.pyc' -delete
	rm -f strawdata.py
	rm -rf __pycache__
	rm -rf classes.dot packages.dot

