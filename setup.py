import os
from setuptools import setup, find_packages

version = '0.6'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

# line breaks are needed after each block so that reST doesn't get mad
long_description = """
%s

%s

%s

%s

""" % (read('README.txt'),
       read('src', 'collective', 'lineage', 'README.txt'),
       read('docs', 'INSTALL.txt'),
       read('docs', 'HISTORY.txt'))

setup(name='collective.lineage',
      version=version,
      description="The microsite creation product for Plone",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone lineage',
      author='Six Feet Up, Inc.',
      author_email='info@sixfeetup.com',
      url='http://plone.org/products/collective-lineage',
      license='GPL',
      packages=find_packages('src'),
	  package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'p4a.z2utils',
          'p4a.common',
          'p4a.subtyper',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
