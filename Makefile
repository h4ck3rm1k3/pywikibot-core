PYTHONPATH=/mnt/data/home/mdupont/experiments/wiki/pywikibot-core:/mnt/data/home/mdupont/experiments/wiki/pywikibot-core/pywikibot:/mnt/data/home/mdupont/.local/lib/python3.3/site-packages/logilab_common-0.60.0-py3.3.egg:/usr/local/lib/python3.3/dist-packages:/mnt/data/home/mdupont/.local/lib/python3.3/site-packages/metadata_manager-0.0001a-py3.3.egg:/mnt/data/home/mdupont/.local/lib/python3.3/site-packages/lxml-3.2.3-py3.3-linux-x86_64.egg:/mnt/data/home/mdupont/.local/lib/python3.3/site-packages/funcparserlib-0.4dev-py3.3.egg:/mnt/data/home/mdupont/.local/lib/python3.3/site-packages/Mock_Nose_Plug_plugin-0.1-py3.3.egg:/usr/local/lib/python3.3/dist-packages/flake8-2.0-py3.3.egg:/usr/local/lib/python3.3/dist-packages/pep8ify-0.0.8-py3.3.egg:/usr/local/lib/python3.3/dist-packages/Flask-0.11_dev_20130809-py3.3.egg:/usr/local/lib/python3.3/dist-packages/itsdangerous-0.23-py3.3.egg:/usr/local/lib/python3.3/dist-packages/Jinja2-2.7.1-py3.3.egg:/usr/local/lib/python3.3/dist-packages/Werkzeug-0.9.3-py3.3.egg:/usr/local/lib/python3.3/dist-packages/MarkupSafe-0.18-py3.3-linux-x86_64.egg:/usr/local/lib/python3.3/dist-packages/Flask_XML_RPC-0.1.2-py3.3.egg:/usr/local/lib/python3.3/dist-packages/logilab_common-0.60.0-py3.3.egg:/usr/local/lib/python3.3/dist-packages/astroid-1.0.0-py3.3.egg:/usr/lib/python3.3:/usr/lib/python3.3/plat-x86_64-linux-gnu:/usr/lib/python3.3/lib-dynload:/mnt/data/home/mdupont/.local/lib/python3.3/site-packages:/usr/lib/python3/dist-packages

PYTHON=PYTHONPATH=$(PYTHONPATH) python3

test :
	-$(PYTHON) tests/dry_api_tests.py
	-$(PYTHON) tests/textlib_tests.py
	-$(PYTHON) tests/page_tests.py
	-$(PYTHON) tests/dry_site_tests.py
	-$(PYTHON) tests/__init__.py
	-$(PYTHON) tests/utils.py
	-$(PYTHON) tests/pwb_tests.py
	-$(PYTHON) tests/i18n/test.py
	-$(PYTHON) tests/i18n/__init__.py
	-$(PYTHON) tests/wikibase_tests.py
	-$(PYTHON) tests/ui_tests.py
	-$(PYTHON) tests/api_tests.py
	-$(PYTHON) tests/pwb/print_locals.py
	-$(PYTHON) tests/site_tests.py
	-$(PYTHON) tests/i18n_tests.py

setuptest:
	PYTHONPATH=/mnt/data/home/mdupont/experiments/wiki/pywikibot-core:/mnt/data/home/mdupont/experiments/wiki/pywikibot-core/pywikibot:/mnt/data/home/mdupont/.local/lib/python3.3/site-packages python3 setup.py test

test2 :
#	PYTHONPATH=. python  pywikibot/login.py
	PYTHONPATH=/mnt/data/home/mdupont/experiments/wiki/pywikibot-core 	python3 pywikibot/login.py

lint:
	- ~/.local/bin/pylint -E --output-format=parseable */*/*.py  */*.py *.py

flakes :
	- ~/.local/bin/pyflakes */*/*.py  */*.py *.py

