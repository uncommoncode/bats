from setuptools import setup
from setuptools import find_packages

setup(
    name='bats',
    version='0.0.1',
    packages=find_packages(),
    author='Emmett McQuinn',
    license='LICENSE.txt',
    description='Beautiful audio tools for interactive data analysis',
    keywords='audio interactive tools pandas',
    test_suite='tests',
    platforms="any",
    python_requires=">=3.6.1",
    install_requires=[
        'numpy >= 1.17.0',
        'scipy >= 1.4.1',
        'matplotlib >= 3.0.0',
    ],
)
