from setuptools import setup, find_packages

VERSION = '0.1'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements-dev.txt') as f:
    dev_requirements = f.read().splitlines()

setup(
    name='PrePy',
    version=VERSION,
    description="""
    PrePy:
    A simple GUI for setting parameters and stimulating
        Pain-evoked potentials via a Raspberry Pi.
    """,
    url='TBD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    scripts=[],
    platforms='any',
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=dev_requirements,
    install_requires=requirements,
    entry_points={}
)
