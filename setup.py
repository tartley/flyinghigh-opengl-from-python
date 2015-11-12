
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        'flyinghigh.engine.render',
        [r'flyinghigh\engine\render.pyx'],
        libraries=['opengl32'],
    ),
]

setup(
    name = 'Render',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
)

