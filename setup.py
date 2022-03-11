import os
from setuptools import setup, find_namespace_packages

requirements = open('requirements.txt').readlines()
with open(os.path.normpath(os.path.join(__file__, '../scraper/VERSION'))) as f:
    __version__ = f.readline(0)


setup(name='dog-scraper',
      version=__version__,
      description='A repo for scrapping dog and pets from Israel Ministry of agriculture',
      url='https://github.com/Omerdan03/dog_scraper.git',
      author='Omer Danziger',
      author_email='Omer.d@razor-labs.com',
      license='MIT License',
      packages=find_namespace_packages(),
      install_requires=requirements,
      package_data={
          '': ['*.txt', '*.json', '*.yml', '*.yaml', 'VERSION', '*.pkl']
      })
