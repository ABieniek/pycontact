""" pycontact setup
by Maximilian Scheurer, Peter Rodenkirch
"""
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

extensions = [Extension("PyContact.cy_modules.cy_gridsearch",
                        ["PyContact/cy_modules/cy_gridsearch.pyx"], language="c++",
                        extra_compile_args=["-std=c++11"],
                        extra_link_args=["-std=c++11"]),
              ]

setup(
    name='pycontact',
    version='0.1.0b',
    description='pycontact - a tool for contact analysis of biomolecules from MD trajectories',
    long_description='',
    url='https://github.com/maxscheurer/pycontact',
    author='Maximilian Scheurer, Peter Rodenkirch',
    author_email='mscheurer@ks.uiuc.edu',
    license='GPLv3',

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='computational biophysics simulation biology bioinformatics visualization protein biomolecules dna',

    package_dir = {'PyContact': 'PyContact'},
    packages=find_packages(),

    install_requires = ['numpy','matplotlib','mdanalysis'],
    ext_modules = cythonize(extensions),

    entry_points={
        'console_scripts': [
            'pycontact=pycontact:main',
        ],
    },

)
