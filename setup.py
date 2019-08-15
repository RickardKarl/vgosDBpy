from setuptools import setup, find_packages

'''
    Currently not in use
'''


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name='vgosDBpy',
    version='1.0.0',
    description='Utilities to visualise and perform simple editing VLBI data in the vgosdDB format.',
    long_description=readme,
    author='Rickard Karlsson, Hanna Ek',
    author_email='rickkarl@student.chalmers.se',
    url='https://github.com/RickardKarl/vgosDBpy',
    license=license,
    packages=find_packages(),
    install_requires = requirements,
    python_requires='>=3.5'
)
