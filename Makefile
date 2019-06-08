PYTHON_FILES = $(shell find . -type f -name "*.py" -not -path "./build/*" -not -path "./.tox/*")
CURRENT_DIR = $(CURDIR)

# Execute as root
setup:
	pip3 install -U pylint pytest pycodestyle yapf --user

test_all:
	python3 -m unittest discover -v -s geekhours/test/

test_database:
	python3 -m unittest -v geekhours/test/test_database.py

test_command:
	python3 -m unittest -v geekhours/test/test_command.py

lint:
	pylint -r n $(PYTHON_FILES)
	pycodestyle --max-line-length=100 $(PYTHON_FILES)
	yapf -d $(PYTHON_FILES)

build:
	python3 setup.py sdist bdist_wheel

tox:
	pip3 install -U tox --user
	tox

clean:
	python3 setup.py clean --all

reinstall:
	make clean
	make build
	pip3 uninstall geekhours
	pip3 install dist/geekhours-0.0.1-py3-none-any.whl

.PHONY: install test_all test_database test_command lint build clean
