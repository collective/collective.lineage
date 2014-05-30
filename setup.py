import os
from setuptools import setup, find_packages

version = '2.0dev'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

# line breaks are needed after each block so that reST doesn't get mad

long_description = '\n\n'.join((read('README.rst'),
                                read('docs', 'INSTALL.rst'),
                                read('CHANGES.rst')))

setup(
    name='collective.lineage',
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
        'Products.CMFCore',
        'five.localsitemanager',
        'plone.app.imaging',
        'plone.app.layout',
        'plone.folder',
        'zope.component',
        'zope.event',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'interlude',
            'plone.app.testing',
            'zope.configuration',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
