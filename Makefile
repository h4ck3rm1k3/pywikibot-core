
setuptest:
	python3 setup.py test

test :
#	PYTHONPATH=. python  pywikibot/login.py
	PYTHONPATH=/mnt/data/home/mdupont/experiments/wiki/pywikibot-core 	python3 pywikibot/login.py

lint:
	- ~/.local/bin/pylint -E --output-format=parseable */*/*.py  */*.py *.py

flakes :
	- ~/.local/bin/pyflakes */*/*.py  */*.py *.py

