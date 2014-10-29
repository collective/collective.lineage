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

Lineage works with Plone 4.1+ and the upcoming Plone 5.


Upgrading to 2.X
================

Lineage `2.0` is a major upgrade to the software and will require you to have
updated to the `1.1.2` version before you migrate any existing Lineage child
sites to the new version. Lineage `2.0` removes all dependancies on
`p4a.subtyper` and makes the product Plone 5 ready. The `1.1.2` release of
Lineage is only used to migrate your existing Lineage `1.1` sites up to the
needed state for the new `2.0` release.

Steps for upgrading:
--------------------

1. Install version `1.1.2` into your existing Lineage powered site
2. Go to the Plone Site Setup and from the Add-Ons panel click the button to
   upgrade the Lineage product
3. Install version `2.0` into your existing Lineage powered site
4. Go to the Plone Site Setup and from the Add-Ons panel click the button to
   upgrade the Lineage product
5. Enjoy Lineage `2.0`


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
5. Click the `Actions` drop down and select `Enable Subsite`. This
   "activates" the child site behavior.
6. The Plone site now has a child site. A drop down will appear at the
   top of the Plone to the left of the site actions area. A user can
   select the parent site or any child sites from this drop down.
