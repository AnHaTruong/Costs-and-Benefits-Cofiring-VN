## What this is about

### Cofiring
Does it make sense for a tropical middle income country to burn rice straw at the coal power plants?

Blending biomass with fossil fuels is a relatively low-cost technology to use renewable energy in the electricity generation sector. Most coal power plants can co-fire a small fraction (<10% energy) of biomass without major retrofit. In high income countries, over a hundred of power plants cofire biomass, often because governments forced utilities to deliver a minimum fraction of their electricity from renewable sources. 

### Key results

This is a financial model of the sector, to study the business and social case for cofiring 5% rice straw with coal, in an old and in a new coal power plant. We compute the costs and benefits for three segments --farmers, reseller and plant owner-- as well as external benefits to society as a whole. We find that there is a weak business case: based on existing coal costs, the willingness to pay of the plant owner is greater than the willingness to accept of the farmer, plus transportation costs. External benefits come from two effects: reducing open air straw burning, and displacing greenhouse gas emissions for coal. Assuming a carbon value of 1$/tCO2, the value of avoided CO2 is small in front of agricultural and air quality benefits.


## Installation

The model is written in  Python 3 with a virtual environment and managed by GNU Make. From a default Ubuntu you will need:

***sudo apt install make***
***sudo apt install python3-venv***

Installation of dependencies into the virtual environment is supposed to happens automagically. Even for the `natu` package, which is the less bad solution to deal with physical units in Python we found.

## Usage

To make all figures and tables, use:
```make```

On first run the Makefile should setup the virtual environment. This includes pulling Pandas (with the xlrd optional Excel import filter), Numpy and Matplotlib libraries, as well as setting up `natu`.  Version 0.1.2 is required with Python 3, since version 0.1.1 is incompatible, its module `core.py` uses the `reduce` function without importing it. Unfortunately the proper version is not in Pypi as of 2020/04, so we install from GitHub.

## Development notes

Dependencies for development are also listed in the file `requirements.txt` . They can be installed system-wide from the distribution repository, but I got burned with Ubuntu's old version of  `pytest` once, so now I prefer to use the Pypi version in the venv.

Code quality is promoted with these practices:

0. Defensive self testing with  `assert`  statements
1. Unit testing with  `doctests`  comments in the code
2. Regression testing with the  `pytest`
3. Format code with `black`.
4. Compliance with Python code conventions is enforced with  `pycodestyle`  (aka pep8) before each commit
5. Compliance with Python in-code documentation is enforced with  `pydocstyle` (aka pep257) before each commit
6. Static code analysis quality is enforced with  `pylint`  before each commit
7. Coherence of computations with respect to physical units is enforced with the  `natu`  package

The `pre-commit` script in the project directory is meant to enforce practices 1 to 6. The script is to be inspected, made executable, and then moved to `.git/hook/pre-commit`. You can call `make install-pre-commit` for that. The precommit hook script is fragile to `git mv` commands. In this case do the tests manually, then commit with -n option.

In addition we did some limited system testing by reproducing previously published LCOE numbers in the MOIT Technology Database.

## Bugs
Known bugs and workarounds:

doctest fails in an spyder3 IPython console with an unexpected argument in __init__
See https://github.com/spyder-ide/spyder/issues/1855
Use a simple Python console instead.

Make does not handle whitespace in PATH. Workaround: use underscores not spaces in directory and file names.

natu 0.1.2 improperly quote a LaTeX escape sequences in core.py:331 and exponents.py:41. This make a silent DeprecationWarning in Python 3.6, a visible DeprecationWarning in Python 3.8 and is expected to cause SyntaxError in Python 3.10. Fix: replace '\,' by r'\\,'.

In `pytest-5.4.1` the modules `doctest` and `coverage` are incompatible and five AttributeError: 'DoctestItem' object has no attribute 'fixturenames'. Workaround: coverage does not include doctests.


## For new developpers

Reminder: there are differences between a python source file and a python module.

+ The module name is the filename, without the `.py` extension.
+ A python source file can sometimes define a script, not a module.

From the filesystem point of view, source files are organised in directories. But from Python's point of view, modules are organised in packages.

+ The package name is the same as directory name.
+ The separator is a dot, since the slanted bar is OS specific.

Modules must be run from the root directory, not from the directory they are in. Otherwise Python does not know the root of the package hierarchy.

+ In a terminal, to run the file `manuscript1/figure2.py` the command is `python3 -m manuscript1.figure2`. 
+ A graphical environment may also need to be told to run modules from the project root directory. Start Spyder3 from the project root directory. When it opens the dialog box "Run settings for X" when you run a file X.py for the first time. In the `Working directory setting`, choose `The current working directory`. 

## For developpers

All imports from natu have to go through model.utils. Import nothing from natu directly.
If a module needs something from natu.units, natu.math or natu.numpy : first import it into model.utils and then get it from there.
This is because we need a single point to control natu.
