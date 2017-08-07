from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="cython_fibonacci",
    ext_modules = cythonize("cython_fibonacci.pyx")
)
