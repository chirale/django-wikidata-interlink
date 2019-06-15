import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wikidata-interlink',
    version='0.1',
    # packages=find_packages(),
    packages=[
        'wikidata_interlink',
        'wikidata_interlink.utils',
    ],
    include_package_data=True,
    license='MIT License',
    description='A Django app to retrieve information about a keyword with the power of SPARQL and Wikidata.',
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/chirale/django-wikidata-interlink',
    author='Emanuele Zangarini',
    author_email='chirale@gmail.com',
    install_requires=[
        'requests>=2.22,<3',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Development Status :: 3 - Alpha',
    ],
)