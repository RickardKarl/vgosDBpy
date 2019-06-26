from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='vgosDBpy',
    version='1.0',
    description='Utilities for vgodDB format handling VLBI data',
    long_description=readme,
    author='Rickard Karlsson, Hanna Ek',
    #author_email='mail@mail.com',
    url='https://github.com/RickardKarl/NVI_vgosDB_openv2',
    license=license,
    packages=find_packages(exclude=('Rickard', 'Hanna'))
)
