from setuptools import setup
import os

with open('README.md') as readme_file:
    long_description = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.in')) as f:
    required = f.read().splitlines()

setup(
    name='Tchou Server',
    version='1.0',
    long_description=long_description,
    packages=['tchou'],
    include_package_data=True,
    zip_safe=False,
    install_requires=required
)
