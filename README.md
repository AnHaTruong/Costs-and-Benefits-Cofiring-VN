## What this is about

### Cofiring

Blending biomass with fossil fuels is a relatively low-cost technology to use renewable energy in the electricity generation sector. Most coal power plants can co-fire a small fraction (<10% energy) of biomass without major retrofit. In high income countries, over a hundred of power plants cofire biomass, often because governments forced utilities to deliver a minimum fraction of their electricity from renewable sources.

### Key results

Would that technology be relevant in Vietnam, a middle income country? Here we study the business case for cofiring 5% rice straw with coal, in an old and in a new coal power plant. We compute the costs and benefits for three segments --farmers, reseller and plant owner-- as well as external benefits to society as a whole. We find that there is a business case: based on existing coal costs, the willingness to pay of the plant owner is greater than the willingness to accept of the farmer, plus transportation costs. External benefits come from two effects: reducing open air straw burning, and displacing greenhouse gas emissions for coal. Assuming a carbon value of 1$/tCO2, the value of avoided CO2 is small in front of agricultural and air quality benefits.


## Installation

The model is written in  Python 3.
It uses pandas, pytest, SALib and other python dependencies listed in the file `requirement.txt`.

Installation should be   ***pip3 install -r requirements.txt***
and then ***sudo apt install pylint, pycodestyle, pydocstyle***

Failing that, here are installation notes:
+ We don't test compatibility with Python 2.
+ `pandas` can be installed from Ubuntu package `python3-pandas`, but the pip version is likely more up to date.
+  `xlrd` can be installed from Ubuntu package  `python3-xlrd`
+ `pytest` can be installed from the Ubuntu package `python3-pytest` but DON'T. That is an old version.
+ `pytest-cov` can be installed from the Ubuntu package `python3-coverage`
+ `SALib can be installed `sudo pip3 install salib` . The sensitivity analysis code was removed in 2019-06, so it should no really be necessary.
+ `natu` version 1.2 is required with Python 3, not in Pypi as of 2017/11, so we install from GitHub
+ If necessary the makefile will install  `.git/hook/pre-commit`  script when doing `make cleaner`.

## Usage

The project is managed with `make`. To make all figures and tables, use:
```make```

## Code quality

Code quality is promoted with these practices:

0. Self testing with  assert  statements
1. Unit testing with  doctests  comments in the code
2. Regression testing with the  pytest
3. System testing (TODO): by reproducing previously published results using their cost numbers
4. Compliance with Python code conventions is enforced with  pycodestyle  (aka pep8) before each commit
5. Compliance with Python in-code documentation is enforced with  pydocstyle  (aka pep257) before each commit
6. Static code analysis quality is enforced with  pylint  before each commit
7. Coherence of computations with respect to physical units is enforced with the  natu  package


## Bugs
Known bugs and workarounds:

doctest fails in an spyder3 IPython console with an unexpected argument in __init__
See https://github.com/spyder-ide/spyder/issues/1855
Use a simple Python console instead.

We use `natu` version 1.2 because version 1.1 is broken with Python 3. Its module  `core.py` uses the `reduce` function without importing it. As an alternative to pip, one can install a local copy with:
```
git clone git@github.com:kdavies4/natu.git
cd natu
pip3 install -e .
```
Doing that will make static code analysis tools like lint cry a lot. Exclude the subdirectory `natu/` from their search path.


## Developer's tips

The source files are organised in directories. From Python's point of view, the modules are organised in packages. Modules must be run from the root directory, not from the directory they are in. 

+ In a terminal, to run the file `manuscript1/figure2.py` the command is `python3 -m manuscript1.figure2`. The module name is the filename, without the `.py` extension. The package name is the directory name. The separator is a dot, since the slanted bar is OS specific.
+ A graphical environment may also need to be told to run modules from the project root directory. Start Spyder3 from the project root directory. When it opens the dialog box "Run settings for X" when you run a file X.py for the first time. In the `Working directory setting`, choose `The current working directory`. 

Import common.utils before importing natu, to have a chance to disable it if needed.

The precommit hook script is fragile to `git mv` commands. In this case do the tests manually, then commit with -n option.
