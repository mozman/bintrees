# build c extensions with distutils
FLAGS = --inplace --force
CMD = setup.py build_ext

py3:
	python3 $(CMD) $(FLAGS)

py2:
	python  $(CMD) $(FLAGS) 

