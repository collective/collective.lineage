#!/bin/sh

# see https://community.plone.org/t/not-using-bootstrap-py-as-default/620
ln -fs plone-5.0.x.cfg buildout.cfg
rm -r ./lib ./include ./local ./bin
virtualenv --clear .
./bin/pip install --upgrade pip setuptools zc.buildout
./bin/buildout
