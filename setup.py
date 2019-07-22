from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name='vgosDBpy',
    version='1.0.0',
    description='Utilities to visualise and edit space geodetic VLBI data in the vgosdDB format',
    long_description=readme,
    author='Rickard Karlsson, Hanna Ek',
    author_email='rickkarl@student.chalmers.se',
    url='https://github.com/RickardKarl/NVI_vgosDB_openv2', # Decide name
    license=license,
    packages=find_packages(exclude=('Rickard', 'Hanna')),
    keywords = 'vgosDB VLBI space-geodesy QT',
    install_requires = requirements,
    python_requires='>=3'
)
