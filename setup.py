from setuptools import find_packages, setup

setup(
    name='lstar',
    version='0.1.0',
    description='Python implementation of lstar automata learning algorithm.',
    url='https://github.com/mvcisback/lstar',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'attrs',
        'dfa',
        'funcy',
    ],
    packages=find_packages(),
)
