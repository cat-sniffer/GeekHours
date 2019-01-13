PTH_FILE = geekhours.pth
PTH_PATH = /usr/lib/python3.5/dist-packages
PYTHON_FILES = $(shell find . -type f -name "*.py" -not -path "./build/*")
CURRENT_DIR = $(CURDIR)

# Execute as root
install:
	mkdir -p $(PTH_PATH)
	echo $(CURRENT_DIR)/lib > $(PTH_PATH)/$(PTH_FILE)

test_all:
	python3 -m unittest discover -v -s test/

test_database:
	python3 -m unittest -v test/test_database.py

test_command:
	python3 -m unittest -v test/test_command.py

lint:
	pylint -r n $(PYTHON_FILES)
	pycodestyle --max-line-length=100 $(PYTHON_FILES)
	yapf -d $(PYTHON_FILES)

.PHONY: install test_all test_database test_command lint
