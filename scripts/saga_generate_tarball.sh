#!/bin/bash

# Author: Manfred Egger
# date 2023-04-22
# version 1 -- for saga version 9.0.1
#
# SAGA contains non-free code that cannot be shipped with fedora. 
# This script downloads the upstream code, removes the non-free 
# parts and generates a fedora-compliant tarball.

set -xe

MAJOR=9
MINOR=4
PATCH=1
VERSION=$MAJOR.$MINOR.$PATCH

DL_URL="https://sourceforge.net/projects/saga-gis/files/SAGA%20-%20${MAJOR}/SAGA%20-%20${VERSION}/saga-${VERSION}.tar.gz"


#clean
rm -rf saga-$VERSION
rm -rf saga-$VERSION.tar.xz
rm -rf saga-$VERSION.tar.gz

#download original tarball
wget $DL_URL

tar xf saga-$VERSION.tar.gz
# cp -pr saga-$VERSION saga-$VERSION-orig


#clean source
#------------

# no commercial use
# http://sourceforge.net/tracker/?func=detail&aid=3407448&group_id=102728&atid=632652
rm saga-$VERSION/saga-gis/src/tools/simulation/sim_fire_spreading/fireLib.*
# no commercial use
rm saga-$VERSION/saga-gis/src/saga_core/saga_api/mat_mRMR.cpp
# unclear license 
rm -r saga-$VERSION/saga-gis/src/tools/projection/pj_geotrans
# unclear license of company logos
rm saga-$VERSION/saga-gis/src/saga_core/saga_gui/res/svg/logo_*
rm saga-$VERSION/saga-gis/src/saga_core/saga_gui/res/xpm/logo_*
#unclear bundled source zips
rm -r saga-$VERSION/saga-gis/src/tools/simulation/sim_hydrology/doc

#create clean tarball
tar cfJ saga-$VERSION.tar.xz saga-$VERSION
