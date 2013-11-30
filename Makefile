lint:
	- ~/.local/bin/pylint -E --output-format=parseable */*/*.py  */*.py *.py

all :
	- ~/.local/bin/pyflakes */*/*.py  */*.py *.py

