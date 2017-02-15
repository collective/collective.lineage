# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '2.1.1'
short_description = u"The microsite creation product for Plone"
long_description = u'\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read()
])


setup(
    name='collective.lineage',
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
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
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
