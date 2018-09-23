PTH_FILE = geekhours.pth
PTH_PATH = /usr/lib/python3.5/dist-packages

install:
	mkdir -p $(PTH_PATH)
	echo $$(pwd)/lib > $(PTH_PATH)/$(PTH_FILE)

test:
	python3 -m unittest -v test/test_database.py

lint:
	-pylint -r n $$(find . -type f -name "*.py")
	-pycodestyle $$(find . -type f -name "*.py")
	-yapf $$(find . -type f -name "*.py")

.PHONY: install test lint
