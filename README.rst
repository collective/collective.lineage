Introduction
============

.. image:: http://www.sixfeetup.com/logos/lineage.gif
   :height: 144
   :width: 220
   :alt: Lineage
   :align: left

Lineage is a Plone product that allows subfolders of a Plone site to
appear as autonomous Plone sites to the everyday user. This hub and
spoke structure allows site administrators to easily manage multiple,
seemingly independent, sub-entity websites in one Plone. Furthermore,
the "parent" site can access and view the content in all the "child"
sites while the child sites only view their own content. The parent site
can also syndicate chosen content to the selected child sites. Lineage
is less complex and easier to manage than a cluster of nested Plone
sites but gives users all the same benefits.

Lineage can be used within a large organization to manage multiple
microsites, such as school district sites, university departments,
corporate product sites, public library satellites,  professional
association events, and more.

Lineage works with Plone 3 and Plone 4.

NOTE: Lineage 1.1 will require Plone >= 4.1


Upgrade from 1.x
================

Please upgrade to most recent 1.x version in the 1.x branch.  Then deinstall
`collective.lineage` and `p4a.subtyper` via the quick installer.  After that
include lineage 2.x in buildout, rerun to install it and install
collective.lineage in your Plone site using the control panel.


Useful links
============

- pypi: http://pypi.python.org/pypi/collective.lineage
- Plone: http://plone.org/products/collective-lineage
- issue tracker: https://github.com/collective/collective.lineage/issues/
- code repository: http://github.com/collective/collective.lineage/


Detailed Documentation
======================

After you've bootstrapped your buildout, installed all the dependencies,
and installed Lineage via Site Setup -> Add on Products, you are ready
to go.

Add a Child Site

1. In Plone, go to the place where you want to add a new child site.
2. Click Add New, and add a `Folder`.
3. Enter the title and description for the Child site.
4. Click Save.
5. Click the `actions` drop down and select `Child Site`. This
   "activates" the child site behavior.
6. The Plone site now has a child site. A drop down will appear at the
   top of the Plone to the left of the site actions area. A user can
   select the parent site or any child sites from this drop down.
