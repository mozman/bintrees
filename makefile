# Author:  mozman
# License: MIT-License

BUILD_OPTIONS = setup.py build_ext --inplace --force
TEST_OPTIONS = -m unittest discover
SRC = bintrees
PYTHON3 = py -3.9
PYPY3 = pypy3

.PHONY: build test testpypy3 packages

build:
	$(PYTHON3) $(BUILD_OPTIONS)

test: build
	$(PYTHON3) $(TEST_OPTIONS)

testpypy3:
	$(PYPY3) $(TEST_OPTIONS)

clean:
	rm -f $(SRC)/cython_trees.c
	rm -f $(SRC)/*.pyd

packages: test
	$(PYTHON3) setup.py bdist_wheel
	$(PYTHON3) setup.py sdist --formats=zip
