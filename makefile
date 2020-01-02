# Author:  mozman
# License: MIT-License

BUILD_OPTIONS = setup.py build_ext --inplace --force
TEST_OPTIONS = -m unittest discover

PYTHON38 = py -3.8
PYTHON37 = py -3.7
PYPY3 = pypy3

build37:
	$(PYTHON37) $(BUILD_OPTIONS)

build38:
	$(PYTHON38) $(BUILD_OPTIONS)

test37:
	$(PYTHON37) $(TEST_OPTIONS)

test38:
	$(PYTHON38) $(TEST_OPTIONS)

testpypy3:
	$(PYPY3) $(TEST_OPTIONS)

buildall: build38 build37

testall: test38 test37 testpypy3

packages:
	$(PYTHON37) setup.py bdist_wheel
	$(PYTHON38) setup.py bdist_wheel
	$(PYTHON38) setup.py sdist --formats=zip
