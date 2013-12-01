all: lint flakes
	echo 

lint:
	~/.local/bin/pylint -E --output-format=parseable  *.py */*.py

flakes :
	~/.local/bin/pyflakes  *.py */*.py

olint1:
	~/.local/bin/pylint -E --output-format=parseable  login.py
