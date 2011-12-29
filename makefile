# build c extensions with distutils
FLAGS = --inplace --force
CMD = setup.py build_ext

py3:
	python3 $(CMD) $(FLAGS)

py2:
	python  $(CMD) $(FLAGS) 

packages:
	python setup.py sdist --formats=zip,gztar
	python setup.py bdist --formats=msi
	python3 setup.py bdist --formats=msi

upload:
	python setup.py sdist --formats=zip,gztar upload
