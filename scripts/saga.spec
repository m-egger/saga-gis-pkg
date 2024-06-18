Name:          saga
Version:       9.4.1
Release:       1%{?dist}
Summary:       SAGA GIS - System for Automated Geoscientific Analyses

License:       GPL-2.0-or-later and LGPL-2.1-or-later

URL:           http://www.saga-gis.org
# Source0:       https://sourceforge.net/projects/saga-gis/files/SAGA%%20-%%208/SAGA%%20-%%20%%{version}/saga-%%{version}.tar.gz

# nonfree content in upstream tarball, link to old saga mailing list message 
# https://sourceforge.net/p/saga-gis/mailman/message/28391147/
# removed:
Source0:       %{name}-%{version}.tar.xz
Source1:       %{name}_generate_tarball.sh

Patch0:        %{name}_logos.patch
Patch1:        %{name}_geotrans.patch


BuildRequires: cmake
BuildRequires: libgomp
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: wxGTK-devel >= 3.2
BuildRequires: proj-devel
BuildRequires: gdal-devel
BuildRequires: libtiff-devel
BuildRequires: unixODBC-devel
BuildRequires: libpq-devel
BuildRequires: jasper-devel
BuildRequires: libharu-devel
# vigra not available for rhel 9
%if 0%{?fedora}
BuildRequires: vigra-devel
%endif
BuildRequires: hdf5-devel
BuildRequires: opencv-devel
BuildRequires: fftw3-devel
BuildRequires: libcurl-devel
BuildRequires: PDAL-devel
BuildRequires: libsvm-devel
BuildRequires: qhull-devel
BuildRequires: swig
BuildRequires: libappstream-glib
BuildRequires: desktop-file-utils
BuildRequires: python3-devel
BuildRequires: dos2unix

%description
SAGA - System for Automated Geoscientific Analyses is a free geographic
information system (GIS) platform supporting raster, vector, tabular and 
point cloud data. SAGA provides access to its tools via GUI,
command line (shell) or its API.  


%package devel
Summary:        SAGA - System for Automated Geoscientific Analyses development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n python3-%{name}
Summary:        SAGA - System for Automated Geoscientific Analyses python3 package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
This python3-%{name} package contains the python3 bindings and libraries for %{name}.

%prep

%setup -q -n saga-%{version}/%{name}-gis

%if 0%{?fedora}
%patch 0 -p2
%patch 1 -p2
%else
%patch0 -p2
%patch1 -p2
%endif

# remove python files for removed libs
rm src/accessories/python/tools/sim_fire_spreading.py
rm src/accessories/python/tools/pj_geotrans.py

#fix line endings: SAGA used mixed dos and unix endings
dos2unix src/accessories/toolchains/*.xml
dos2unix src/accessories/python/*.py
dos2unix src/accessories/python/data/*.py
dos2unix src/accessories/python/tools/*.py

#fix python shebang: SAGA uses /usr/bin/env python
%py3_shebang_fix src/accessories/python/*.py
%py3_shebang_fix src/accessories/python/data/*.py
%py3_shebang_fix src/accessories/python/tools/*.py

%build
%cmake -DCMAKE_BUILD_TYPE=RELEASE \
    -DWITH_EXCERCISES=OFF \
    -DWITH_DEV_TOOLS=OFF \
    -DWITH_SYSTEM_SVM=ON \
    -DWITH_FIRE_SPREADING=OFF \
    -DWITH_MRMR=OFF \
    -DWITH_CLIPPER_ONE=OFF \
    -DWITH_TOOLS_PDAL=ON \
    -DWITH_PYTHON=ON

%cmake_build

%install
%cmake_install
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/org.saga-gis.saga-gui.appdata.xml
# install german language file
install src/saga_core/saga_gui/res/saga.ger.txt  %{buildroot}/%{_datadir}/%{name} 
#remove some icons and pixmaps folder
rm -rf %{buildroot}%{_datadir}/icons/hicolor/{8x8,72x72,80x80,192x192}/
rm -rf %{buildroot}%{_datadir}/pixmaps

%ldconfig_scriptlets


%files
%defattr(644,root, root, -)
%doc readme.md
%license src/gpl.txt src/lgpl.txt
%{_datadir}/%{name}/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/org.saga-gis.saga-gui.appdata.xml
%{_mandir}/man1/%{name}_*1*

%defattr(-,root, root, -)
%{_bindir}/%{name}_cmd
%{_bindir}/%{name}_gui
%{_libdir}/%{name}/*
%{_libdir}/lib%{name}_api.so.*
%{_libdir}/lib%{name}_gdi.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}_api.so
%{_libdir}/lib%{name}_gdi.so

%files -n python3-%{name}
%{python3_sitearch}/PySAGA/_saga_api.so
%{python3_sitearch}/PySAGA/saga_api.py
%{python3_sitearch}/PySAGA/__init__.py
%{python3_sitearch}/PySAGA/helper.py
%{python3_sitearch}/PySAGA/convert.py
%{python3_sitearch}/PySAGA/plot.py
%{python3_sitearch}/PySAGA/__pycache__/*.pyc
%{python3_sitearch}/PySAGA/tools/*.py
%{python3_sitearch}/PySAGA/tools/__pycache__/*.pyc
%{python3_sitearch}/PySAGA/data/*.py
%{python3_sitearch}/PySAGA/data/__pycache__/*.pyc


%changelog
* Mon Jun 17 2024 Manfred Egger - 9.4.1-1
- Update to 9.4.1
- Remove patch for file io bug, fixed upstream

* Mon May 13 2024 Manfred Egger - 9.4.0-2
- added patch to fix file io bug

* Mon Apr 15 2024 Manfred Egger - 9.4.0-1
- Update to 9.4.0
- remove executable permission for python files

* Tue Mar 12 2024 Manfred Egger - 9.3.2-1
- Update to 9.3.2
- remove swig patch, included upstream (bug #317)

* Thu Feb 29 2024 Manfred Egger - 9.3.1-2
- added fixes for RHEL 9
- added swig patch (bug #317)

* Wed Jan 24 2024 Manfred Egger - 9.3.1-1
- Update to 9.3.1

* Mon Dec 18 2023 Manfred Egger - 9.3.0-1
- Update to 9.3.0
- fixed line endings for python scripts and toolchains
- fixed file permissions for python scripts
- added dos2unix as build dependency

* Mon Oct 09 2023 Manfred Egger - 9.2.0-1
- Update to 9.2.0
- Drop python patch, included upstream (bug #304)
- Restuctured python section in spec file

* Wed Sep 13 2023 Manfred Egger - 9.1.2-1
- Update to 9.1.2

* Wed Aug 02 2023 Manfred Egger - 9.1.1-1
- Update to 9.1.1

* Sun Jul 23 2023 Manfred Egger - 9.1.0-1
- Update to 9.1.0
- Build with new default python structure PySAGA
- Fixed python3 package naming according to scheme

* Wed Jul 5 2023 Manfred Egger - 9.0.3-1
- Update to 9.0.3

* Sat Jul 01 2023 Manfred Egger - 9.0.2-2
- Build with Clipper 2

* Thu Jun 01 2023 Manfred Egger - 9.0.2-1
- Update to 9.0.2

* Mon Apr 24 2023 Manfred Egger - 9.0.1-1
- Initial packaging
