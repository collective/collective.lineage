from pathlib import Path
from setuptools import setup

version = "4.0.0"
short_description = "The microsite creation product for Plone"
long_description = "\n\n".join(
    [Path("README.rst").read_text(), Path("CHANGES.rst").read_text()]
)


setup(
    name="collective.lineage",
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone lineage",
    author="Six Feet Up, Inc.",
    author_email="info@sixfeetup.com",
    url="https://pypi.org/project/collective-lineage",
    license="GPL",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "Zope",
        "Products.CMFCore",
        "five.localsitemanager",
        "plone.browserlayer",
        "plone.folder",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes",
            "plone.dexterity",
            "plone.testing>=5.0.0",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
