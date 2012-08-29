import os
from setuptools import setup, find_packages

version = '1.0'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

# line breaks are needed after each block so that reST doesn't get mad

long_description = '\n\n'.join((read('README.rst'),
                                read('docs', 'INSTALL.rst'),
                                read('docs', 'HISTORY.rst')))

setup(name='collective.lineage',
      version=version,
      description="The microsite creation product for Plone",
      long_description=long_description,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone lineage',
      author='Six Feet Up, Inc.',
      author_email='info@sixfeetup.com',
      url='http://plone.org/products/collective-lineage',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'p4a.z2utils',
          'p4a.common',
          'p4a.subtyper>=1.2.0',
          'plone.app.registry',
      ],
      extras_require={
          'test': [
              'interlude',
              'plone.app.testing',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
