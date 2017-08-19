
# uncomment to enable bootstrap mode
#global bootstrap 1

%if !0%{?bootstrap}
%global tests 1
%endif

Name:    dolphin
Summary: KDE File Manager
Version: 17.04.1
Release: 1%{?dist}

License: GPLv2+
URL:     https://cgit.kde.org/%{name}.git/
%global revision %(echo %{version} | cut -d. -f3)
%global majmin_ver %(echo %{version} | cut -d. -f1,2)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

Patch0: dolphin-17.04.1-allow-root.patch

BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  cmake(KF5DocTools)
BuildRequires:  cmake(KF5Init)
BuildRequires:  cmake(KF5KCMUtils)
BuildRequires:  cmake(KF5NewStuff)
BuildRequires:  cmake(KF5CoreAddons)
BuildRequires:  cmake(KF5I18n)
BuildRequires:  cmake(KF5DBusAddons)
BuildRequires:  cmake(KF5Bookmarks)
BuildRequires:  cmake(KF5Config)
BuildRequires:  cmake(KF5KIO)
BuildRequires:  cmake(KF5Parts)
BuildRequires:  cmake(KF5Solid)
BuildRequires:  cmake(KF5IconThemes)
BuildRequires:  cmake(KF5Completion)
BuildRequires:  cmake(KF5TextWidgets)
BuildRequires:  cmake(KF5Notifications)
BuildRequires:  cmake(KF5Crash)

BuildRequires:  phonon-qt5-devel

%if ! 0%{?bootstrap}
BuildRequires:  kf5-kactivities-devel
BuildRequires:  kf5-baloo-devel
BuildRequires:  kf5-kfilemetadata-devel
BuildRequires:  baloo-widgets-devel >= %{majmin_ver}
%endif

%if 0%{?tests}
BuildRequires: xorg-x11-server-Xvfb
# for %%check
BuildRequires:  libappstream-glib
%endif

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%{?kf5_kinit_requires}

Recommends:     kio-extras%{?_isa}

# translations moved here
Conflicts: kde-l10n < 17.03

%description
%{summary}.

%package        libs
Summary:        Dolphin runtime libraries
Requires:       %{name} = %{version}-%{release}
%description    libs
%{summary}.

%package        devel
Summary:        Developer files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
Requires:       kf5-kio-devel%{?_isa}
%description    devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. \
  -DBUILD_TESTING:BOOL=%{?tests:ON}%{!?tests:OFF}
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang dolphin --with-html


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf5_datadir}/appdata/org.kde.%{name}.appdata.xml ||:
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop ||:
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a \
make test ARGS="--output-on-failure --timeout 10" -C %{_target_platform} ||:
%endif


%posttrans
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
update-desktop-database -q &> /dev/null ||:
fi

%files -f dolphin.lang
%license COPYING*
%doc README
%{_kf5_bindir}/%{name}
%{_kf5_bindir}/servicemenuinstallation
%{_kf5_bindir}/servicemenudeinstallation
%{_sysconfdir}/xdg/servicemenu.knsrc
%{_kf5_libdir}/libkdeinit5_dolphin.so
%{_kf5_datadir}/kservices5/kcmdolphin*.desktop
%{_kf5_datadir}/config.kcfg/dolphin_*
%{_datadir}/dbus-1/services/org.kde.dolphin.FileManager1.service
%{_kf5_datadir}/appdata/org.kde.%{name}.appdata.xml
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%{_kf5_datadir}/kservicetypes5/fileviewversioncontrolplugin.desktop
%{_kf5_datadir}/kxmlgui5/%{name}/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libdolphinprivate.so.*
%{_kf5_libdir}/libdolphinvcs.so.*
%{_kf5_qtplugindir}/kcm_*.so
%{_kf5_datadir}/kxmlgui5/dolphinpart/
%{_kf5_qtplugindir}/dolphinpart.so
%{_kf5_datadir}/kservices5/dolphinpart.desktop

%files devel
%{_includedir}/Dolphin/
%{_includedir}/dolphin*_export.h
%{_kf5_libdir}/cmake/DolphinVcs/
%{_kf5_libdir}/libdolphinvcs.so
%{_datadir}/dbus-1/interfaces/org.freedesktop.FileManager1.xml


%changelog
* Wed May 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.04.1-1
- 17.04.1

* Sat Apr 22 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.04.0-2
- use %%find_lang for HTML handbooks

* Fri Apr 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.04.0-1
- 17.04.0, +translations, cmake-style kf5 deps

* Wed Mar 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 16.12.3-1
- 16.12.3

* Wed Feb 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 16.12.2-1
- 16.12.2

* Tue Jan 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 16.12.1-1
- 16.12.1, update URL

* Mon Dec 26 2016 Rex Dieter <rdieter@math.unl.edu> - 16.12.0-1
- 16.12.0, support bootstrap, %%check: enable tests

* Wed Nov 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.3-1
- 16.08.3

* Thu Oct 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.2-1
- 16.08.2

* Tue Sep 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.1-1
- 16.08.1

* Thu Sep 01 2016 Rex Dieter <rdieter@fedoraproject.org> 16.08.0-2
- update URL (#1325154)

* Fri Aug 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.0-1
- 16.08.0

* Fri Aug 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.07.90-2
- Recommends: kio-extras (#1366585)

* Sat Aug 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.07.90-1
- 16.07.90

* Fri Jul 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.07.80-1
- 16.07.80

* Fri Jul 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.3-1
- 16.04.3

* Sun Jun 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.2-1
- 16.04.2

* Sun May 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.1-1
- 16.04.1

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.0-1
- 16.04.0

* Sun Mar 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.3-1
- 15.12.3

* Sun Feb 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.2-1
- 15.12.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Rex Dieter <rdieter@fedoraproject.org> 15.12.1-2
- cosmetics, tighten BR: baloo-widgets, -BR: cmake

* Mon Jan 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.1-1
- 15.12.1

* Fri Jan 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.0-2
- %kf5_kinit_requires (#1294982), cosmetics
- libs: move remaining plugins here, drop (arch'd) dep on main pkg

* Sun Dec 20 2015 Rex Dieter <rdieter@fedoraproject.org> 15.12.0-1
- 15.12.0

* Tue Nov 17 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.3-1
- 15.08.3

* Tue Sep 15 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.1-1
- 15.08.1
- cosmetics, move dolphinpart to -libs
- relax BR on baloo-widgets

* Mon Aug 31 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Reviving Dolphin stand-alone package (#1258430)
