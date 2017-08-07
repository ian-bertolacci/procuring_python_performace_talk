
all: cython_fibonacci.so cython_jacobi.so

%.so : %_setup.py %.pyx
	python $< build_ext --inplace

clean-build:
	- /bin/rm -r build *.c

clean-bin:
	- /bin/rm *.so

clean: clean-bin clean-build
