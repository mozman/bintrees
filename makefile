# Author:  mozman
# License: MIT-License

BUILD_OPTIONS = setup.py build_ext --inplace --force
TEST_OPTIONS = -m unittest discover

PYTHON27 = py -2.7
PYTHON35 = py -3.5
PYTHON36 = py -3.6
PYPY = C:\pypy2-5.6.0\pypy.exe

build27:
	$(PYTHON27)  $(BUILD_OPTIONS)

build35:
	$(PYTHON35) $(BUILD_OPTIONS)

build36:
	$(PYTHON36) $(BUILD_OPTIONS)

test27:
	$(PYTHON27) $(TEST_OPTIONS)

test35:
	$(PYTHON35) $(TEST_OPTIONS)

test36:
	$(PYTHON36) $(TEST_OPTIONS)

testpypy:
	$(PYPY) $(TEST_OPTIONS)

buildall: build27 build35 build36

testall: test27 test35 test36 testpypy

packages:
	$(PYTHON27) setup.py sdist --formats=zip
	$(PYTHON27) setup.py bdist_wheel
	$(PYTHON27) setup.py bdist --formats=wininst
	$(PYTHON35) setup.py bdist_wheel
	$(PYTHON35) setup.py bdist --formats=wininst
	$(PYTHON36) setup.py bdist_wheel
	$(PYTHON36) setup.py bdist --formats=wininst


release:
	$(PYTHON27) setup.py sdist --formats=zip upload
	$(PYTHON27) setup.py bdist_wheel upload
	$(PYTHON27) setup.py bdist --formats=wininst upload
	$(PYTHON35) setup.py bdist_wheel upload
	$(PYTHON35) setup.py bdist --formats=wininst upload
	$(PYTHON36) setup.py bdist_wheel upload
	$(PYTHON36) setup.py bdist --formats=wininst upload
