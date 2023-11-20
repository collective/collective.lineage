from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "3.0.0.dev0"
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
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone lineage",
    author="Six Feet Up, Inc.",
    author_email="info@sixfeetup.com",
    url="https://pypi.org/project/collective-lineage",
    license="GPL",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "Products.CMFCore",
        "Products.CMFPlone",
        "five.localsitemanager",
        "plone.browserlayer",
        "plone.dexterity",
        "plone.folder",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.testing>=5.0.0",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
