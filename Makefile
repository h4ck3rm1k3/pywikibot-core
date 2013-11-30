test :
#	PYTHONPATH=. python  pywikibot/login.py
	PYTHONPATH=. python3  pywikibot/login.py

lint:
	- ~/.local/bin/pylint -E --output-format=parseable */*/*.py  */*.py *.py

flakes :
	- ~/.local/bin/pyflakes */*/*.py  */*.py *.py

