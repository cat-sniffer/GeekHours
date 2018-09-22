PTH_FILE = geekhours.pth
PTH_PATH = /usr/lib/python3.5/dist-packages

install:
	mkdir -p $(PTH_PATH)
	echo $$(pwd)/lib > $(PTH_PATH)/$(PTH_FILE)

test:
	python3 -m unittest -v test/test_database.py

.PHONY: install test
