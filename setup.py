from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

setup(
    name = "On-the-Fly Gridder",
    ext_modules = cythonize("src/*.pyx", include_path = [np.get_include()]),
    include_dirs = [np.get_include()]
)
