from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="cython_jacobi",
    ext_modules = cythonize("cython_jacobi.pyx")
)
