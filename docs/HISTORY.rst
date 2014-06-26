Changelog
=========

1.1.1 - (2014-06-26)
--------------------

- Add an adapter to allow the child site to use the portal image
  scales. Fixes https://github.com/collective/collective.lineage/issues/18
  [ableeb]

- Remove componentregistry ``collective.lineage.childsite`` utility from the
  component registry.
  [thet]

- Add Chinese translations.
  [adam139]

1.1 - (2013-06-02)
---------------------

- Fixed imports to allow lineage to be compatible with
  Plone >= 4.1
  [calvinhp]

- Update dependencies and import locations and make
  collective.lineage compatible with Plone 4.3.
  [thet]

- Add new events for ``WillBe`` created and removed. This will make
  add-ons like lineage.registry able to properly deal with the child
  site before the component registry is removed.
  [claytron]

- Restored Plone 3.3 compatibility (if plone.app.registry is present)
  [keul]

- i18n fixes and added italian translation
  [keul]

- Uninstall step fixed (closed #8 and #11) but also removed other stuff
  left behind
  [keul]

1.0.1 - (2012-10-13)
--------------------

- Remove ``setup_site`` from the ``install`` function since this is no
  longer needed. Also bumped the metadata version so that the upgrade
  step actually runs.
  [claytron]

- PEP8
  [clayton]

1.0 - (2012-10-08)
------------------

- PEP8 and pyflakes cleanup
  [claytron]

- modernized tests, using layers now.
  [jensens]

- fixed failing test with subscribers, subtype added event is not an object 
  event!
  [jensens]

- moved code to github and increased Plone version used in integrated buildout 
  to 4.1-latest.
  [jensens]

- The subscribers are now registered to the IChildSite interface so
  that custom child site types are still made into IObjectManagerSites.
  [rossp]

- Added an ``isChildSite`` method to the ``LineageUtils`` view, to determine if
  the current context is part of a child site.
  [davidblewett]

- Id attribute added to the lineage selection form to make Diazo/XDV theming
  easier.
  [timo]

- German translation added.
  [timo]

- added support for plone domain
  [macagua]

- Added Spanish translation
  [macagua]

- Changed the ``collective.lineage.childsite`` component to use the
  ``IFolderishContentTypeDescriptor`` interface instead of
  ``IPortalTypedFolderishDescriptor``, allowing any folderish type to become
  a child site.
  [davidblewett]

- Fixed issue where deactivating a Child Site wouldn't remove it from the
  Lineage dropdown menu
  [calvinhp]

- Format README so that it fits within 72 columns.
  [claytron]


0.6.1 - (2011-01-12)
--------------------

- Making sure that we copy the fact that the item inherits from its parent or not
  [lucielejard]

- Updated the ignores
  [lucielejard]

- Fixed the upgrade so that when we grab the layout of a folder, it does not 
  get it using acquisition if it doesn't have one, fixes #18
  [lucielejard]

- Copy over sharing settings from child folder to new folder, fixes #38
  [anthonygerrard]

- Fix by not renaming the child folder, instead create new folder with temp 
  id and rename that to the child folder id after the child folder has been
  deleted, fixes #37
  [anthonygerrard]

- Adding a failing test case for #37 here as it is a serious bug but I have 
  no idea how to fix it
  [anthonygerrard]

- In lineage 0.1 child folders never inherited their parent's portlets so 
  always block parent portlets when migrating, fixes #34
  [anthonygerrard]

- Added a warning if portlet manager is not available on the new folder, 
  fixes #35
  [anthonygerrard]

- Copy portlet assignments from and blocking settings across on migration, 
  fixes #34
  [anthonygerrard]

- Refactor tests so that migration tests are in their own class and so can 
  have common setup logic
  [anthonygerrard]
 
- Read the default page of the child folder before conversion and then set 
  it afterwards, fixes #18
  [anthonygerrard]


0.6 - (2010-05-25)
------------------

- used z3c.autoinclude and removed the zcml slug in buildout.cfg
  [tbesluau]

- update the security settings at the end of the migration so
  that the workflow is applied correctly on the new migrated
  folders, fixes #20
  [lucielejard]

- updated the migration so it keeps the layout on the folder
  fixes #18
  [lucielejard]


0.5.1 - (2010-05-12)
--------------------

- updated docs as per duffyd suggestions
  [lucielejard]


0.5 - (2010-05-11)
------------------

- updated docs with links to the branches created by
  duffyd for the backports of the plip #234 mods to
  Plone 3.1.7
  [lucielejard]


0.4 - (2010-04-30)
------------------

- updated docs about PLIP

- Update docs with information about "activation" behavior.
  [clayton]


0.3 - (2010-04-30)
------------------

- getting the unit testing to work with plone4 and allowing 
  childsite editing with plone4, refs #16 [tbesluau]

- updated README.txt with useful links [lucielejard]

- added tests for the uninstall of lineage [lucielejard]

- updated the list of items todo, removed rolemap.xml since
  we don't use it anymore, updated the history with the recent
  changes [lucielejard]

- moved the registration of the utility in component registry so 
  it gets registered locally, this fixes #5 [lucielejard]

- added a deprecation warning on the Child Folder type
  [lucielejard]

- put back some old zcml so the Child Folder migration can be tested
  [lucielejard]

- added a test for the migration from 0.1 to >0.1
  [lucielejard]

- updated the version in metadata.xml for the upgrade step
  [lucielejard]

- made the Child Folder type not globally addable
  [lucielejard]

- added an upgrade step that will migrate the old Child Folder objects
  [lucielejard]

- added an import various step so that the upgrade step gets run 
  automatically on reinstall
  [lucielejard]

- Set up for i18n translations
  [claytron]

- Moving over to an 'activation' based system instead of having a
  'Child Folder' type.  Now a folder will have the option for a
  subtype named 'Child Site'.
  http://plone.org/products/collective-lineage/issues/3
  http://plone.org/products/collective-lineage/issues/1
  [claytron]

- Remove 'Child Folder' add/edit interfaces.  The type still remains
  so that we can do a migration.
  [claytron]

- Added uninstall profile and hooked it up to the Quickinstaller
  [claytron]

- Added subtyper.xml to the uninstall profile that will deactivate
  all 'Child Sites' in the portal.  This depends on p4a.subtyper
  code that has not yet been released.  This also solves the
  export/import issue
  http://plone.org/products/collective-lineage/issues/2
  [claytron]

- Added a subscriber to create the local component site (this was
  in the 'Child Folder' type before)
  [claytron]


0.2 - (2010-04-08)
------------------

- Doc clarifications
  [claytron]


0.1 - (2009-02-10)
------------------

- Initial public release


Special Thanks
==============

Six Feet Up would especially like to thank Martin Aspeli for his
inspiration and the Duke Clinical Research Institute group for project
funding.
