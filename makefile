# Author:  mozman
# License: MIT-License

BUILD_OPTIONS = setup.py build_ext --inplace --force
TEST_OPTIONS = -m unittest discover

PYTHON36 = py -3.6
PYTHON37 = py -3.7
PYPY3 = pypy3

build36:
	$(PYTHON36) $(BUILD_OPTIONS)

build37:
	$(PYTHON37) $(BUILD_OPTIONS)

test36:
	$(PYTHON36) $(TEST_OPTIONS)

test37:
	$(PYTHON37) $(TEST_OPTIONS)

testpypy3:
	$(PYPY3) $(TEST_OPTIONS)

buildall: build36 build37

testall: test36 test37 testpypy3

packages:
	$(PYTHON36) setup.py sdist --formats=zip,gztar
	$(PYTHON36) setup.py bdist_wheel
	$(PYTHON37) setup.py bdist_wheel
