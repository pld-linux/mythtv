# TODO
# - CFLAGS doesn't get passed
# - bconds broken?
# - mythtv user
# - what about Patch0?
#
# Specfile for MythTV
#
#  MythTV now uses a fairly intelligent cpu-detection script, so if you are
#  building an rpm by hand on the machine it will be used on, I encourage you
#  to use "--with cpu_autodetect" to let mythtv decide for you.
#
#
# Conditional build:
%bcond_with	lirc		# lirc support
%bcond_without	alsa		# alsa support
%bcond_without	oss		# oss
%bcond_with	opengl_vsync	# opengl vsync
%bcond_with	arts		# arts support
%bcond_with	xvmc		# xvmc support
%bcond_with	cpu_autodetect	# enable CPU autodetection at compile time
#
Summary:	A personal video recorder (PVR) application
Summary(pl):	Osobista aplikacja do nagrywania obrazu (PVR)
Name:		mythtv
Version:	0.18.1
#define _snap 20050326
Release:	0.1
License:	GPL v2
Group:		Applications/Multimedia
Source0:	http://www.mythtv.org/mc/%{name}-%{version}.tar.bz2
# Source0-md5:	e6cabf88feeaf6ae8f830d3fdf7b113d
Source1:	mythbackend.sysconfig
Source2:	mythbackend.init
Source3:	mythbackend.logrotate
Patch0:		%{name}-configure.patch
URL:		http://www.mythtv.org/
BuildRequires:	XFree86-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{?with_arts:BuildRequires:	arts-devel >= 13:0.9.5}
BuildRequires:	desktop-file-utils
BuildRequires:	freetype-devel >= 1:2.0.0
BuildRequires:	gcc-c++
BuildRequires:	lame-libs-devel
BuildRequires:	linux-libc-headers >= 7:2.6.10
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	mysql-devel
%{?with_xvmc:BuildRequires:	nvidia-graphics-devel}
%{?with_opengl_vsync:BuildRequires:	nvidia-graphics-devel}
BuildRequires:	qmake >= 6:3.2.1-4
BuildRequires:	qt-devel >= 6:3.2.1-4
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
# ???
ExclusiveArch:	i386 i686 athlon %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	uid	149
%define	gid	149

%description
MythTV implements the following PVR features, and more, with a unified
graphical interface:

 - Basic 'live-tv' functionality. Pause/Fast Forward/Rewind "live" TV.
 - Video compression using RTjpeg or MPEG-4
 - Program listing retrieval using XMLTV
 - Themable, semi-transparent on-screen display
 - Electronic program guide
 - Scheduled recording of TV programs
 - Resolution of conflicts between scheduled recordings
 - Basic video editing

%description -l pl
MythTV implementuje nastêpuj±ce mo¿liwo¶ci PVR, a nawet wiêcej, wraz z
ujednoliconym interfejsem graficznym:
- podstawowa funkcjonalno¶æ "live-tv"; pauza, szybkie przewijanie,
  przewijanie "¿ywej" telewizji
- kompresja obrazu przy u¿yciu RTjpeg lub MPEG-4
- odczyt listy programów przy u¿yciu XMLTV
- pseudoprzezroczyste wy¶wietlanie na obrazie (OSD) z obs³ug± motywów
- elektroniczny przewodnik po programie
- planowane nagrywanie programów telewizyjnych
- rozwi±zywanie konfliktów miêdzy planowanymi nagraniami
- podstawowa edycja obrazu

%package backend
Summary:	Server component of mythtv (a PVR)
Summary(pl):	Czê¶æ serwerowa mythtv (PVR)
Group:		Applications/Multimedia
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	mythtv = %{version}-%{release}
Provides:	user(mythtv)
Provides:	group(mythtv)
Conflicts:	xmltv-grabbers < 0.5.34

%description backend
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the server software, which provides video
and audio capture and encoding services. In order to be useful, it
requires a mythtv-frontend installation, either on the same system or
one reachable via the network.

%description backend -l pl
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
ogl±dania programów telewizyjnych. Wiêcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko oprogramowanie serwerowe, udostêpniaj±ce
us³ugi przechwytywania i kodowania obrazu i d¼wiêku. Aby by³o
przydatne, wymaga instalacji mythtv-frontend - na tym samym systemie,
albo innym osi±galnym po sieci.

%package frontend
Summary:	Client component of mythtv (a PVR)
Summary(pl):	Czê¶æ kliencka mythtv (PVR)
Group:		Applications/Multimedia
Requires:	mythtv = %{version}-%{release}
Requires:	mythtv-themes = %{version}-%{release}
Provides:	mythtv-frontend-api = %(echo %{version} | cut -d. -f1,2)

%description frontend
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the client software, which provides a
front-end for playback and configuration. It requires access to a
mythtv-backend installation, either on the same system or one
reachable via the network.

%description frontend -l pl
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
ogl±dania programów telewizyjnych. Wiêcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko oprogramowanie klienckie, dostarczaj±ce
frontend do odtwarzania i konfiguracji. Wymaga dostêpu do instalacji
mythtv-backend - na tym samym systemie, albo innym osi±galnym po
sieci.

%package setup
Summary:	Setup the mythtv backend
Summary(pl):	Konfigurator backendu mythtv
Group:		Applications/Multimedia
Requires:	mythtv-backend = %{version}-%{release}
Requires:	mythtv-themes = %{version}-%{release}
Provides:	mythtvsetup

%description setup
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the setup software for configuring the
mythtv backend.

%description setup -l pl
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
ogl±dania programów telewizyjnych. Wiêcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko program do konfigurowania backendu mythtv.

%package themes
Summary:	Base themes for mythtv's frontend
Summary(pl):	Podstawowe motywy dla frontendu mythtv
Group:		Applications/Multimedia
Obsoletes:	mythtv-theme-Titivillus

%description themes
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the base themes used by the frontend and
mythtvsetup.

%description themes -l pl
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
ogl±dania programów telewizyjnych. Wiêcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko podstawowe motywy u¿ywane przez frontend oraz
mythtvsetup.

%package -n libmyth
Summary:	Library providing mythtv support
Summary(pl):	Biblioteka udostêpniaj±ca obs³ugê mythtv
Group:		Libraries
Requires:	freetype >= 1:2.0.0
Requires:	lame
Requires:	qt >= 6:3.2.1-4
Requires:	qt-plugin-mysql >= 6:3.2.1-4

%description -n libmyth
Common library code for MythTV and add-on modules (development) MythTV
provides a unified graphical interface for recording and viewing
television programs. Refer to the mythtv package for more information.

%description -n libmyth -l pl
Wspólny kod biblioteki dla MythTV i dodatkowych modu³ów MythTV
dostarczaj±cy ujednolicony interfejs graficzny do nagrywania i
ogl±dania programów telewizyjnych. Wiêcej informacji w pakiecie
mythtv.

%package -n libmyth-devel
Summary:	Development files for libmyth
Summary(pl):	Pliki nag³ówkowe libmyth
Group:		Development/Libraries
Requires:	libmyth = %{version}-%{release}
# ??? Requires???
#BuildRequires:	freetype-devel >= 1:2.0.0
#BuildRequires:	lame-libs-devel
#BuildRequires:	qt-devel >= 6:3.2.1-4
#BuildRequires:	mysql-devel
#BuildRequires:	DirectFB-devel
#%if %{with alsa}
#BuildRequires:	alsa-lib-devel
#%endif
#%if %{with lirc}
#BuildRequires:	lirc-devel
#%endif
#%if %{with arts}
#BuildRequires:	arts-devel >= 13:0.9.5
#%endif

%description -n libmyth-devel
This package contains the header files for developing add-ons for
mythtv.

%description -n libmyth-devel -l pl
Ten pakiet zawiera pliki nag³ówkowe do tworzenia dodatków dla mythtv.

%package -n libmyth-static
Summary:	Static libmyth library
Summary(pl):	Statyczna biblioteka libmyth
Group:		Development/Libraries
Requires:	libmyth-devel = %{version}-%{release}

%description -n libmyth-static
Static libmyth library.

%description -n libmyth-static -l pl
Statyczna biblioteka libmyth.

%prep
%setup -q
#%patch0 -p1

%build
export QTDIR="%{_prefix}"
export QMAKESPEC="linux-g++"
export CFLAGS="%{rpmcflags} -fomit-frame-pointer"

# BTW: this is not autoconf configure
%configure \
    --compile-type=%{?debug:debug}%{!?debug:release} \
    --disable-audio-jack \
    --enable-dvb --dvb-path=%{_includedir} \
%if %{with cpu_autodetect}
    %ifarch i386 i686
		--cpu=i386 --tune=pentium4 --enable-mmx \
    %endif
    %ifarch athlon
        --arch=athlon \
    %endif
    %ifarch %{x8664}
        --arch=x86_64 \
    %endif
%endif
	--%{?with_arts:en}%{!?with_arts:dis}able-audio-arts \
	--%{?with_alsa:en}%{!?with_alsa:dis}able-audio-alsa \
	--%{?with_oss:en}%{!?with_oss:dis}able-audio-oss \
	--%{?with_opengl_vsync:en}%{!?with_openvl_vsync:dis}able-opengl-vsync \
	--%{?with_lirc:en}%{!?with_lirc:dis}able-lirc \
	%{?with_xvmc:--enable-xvmc --enable-xvmc-vld} \
	%{!?with_xvmc:--disable-xvmc --disable-xvmc-vld} \
#  --disable-joystick-menu \
#  --disable-firewire \
#  --disable-ivtv \
#  --enable-dvb-eit \

#sed -i -e 's:OPTFLAGS=.*:OPTFLAGS=%{rpmcflags} -Wno-switch:g' config.mak
# dunno. the configure doesn't take --prefix...
sed -i -e 's:PREFIX =.*:PREFIX = %{_prefix}:g' settings.pro

# MythTV doesn't support parallel builds
#qmake -o Makefile mythtv.pro \
#    QMAKE_CXX="%{__cxx}" \
#    QMAKE_LINK="%{__cxx}" \
#    QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}"

qmake mythtv.pro

%{__make} qmake

# We don't want rpm to add perl requirements to anything in contrib
find contrib -type f | xargs -r chmod a-x

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

export QTDIR="%{_prefix}"
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the files that we added on top of mythtv's own stuff
install -pD %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/mythbackend
install -pD %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mythbackend
install -pD %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/mythbackend

# Desktop entries
#mkdir -p %{buildroot}%{_datadir}/pixmaps
#mkdir -p %{buildroot}%{_datadir}/applications
#for file in %{desktop_applications}; do
#  install -p %{_sourcedir}/$file.png %{buildroot}%{_datadir}/pixmaps/$file.png
#  desktop-file-install --vendor %{desktop_vendor} \
#    --dir %{buildroot}%{_datadir}/applications    \
#    --add-category X-Red-Hat-Extra                \
#    --add-category Application                    \
#    --add-category AudioVideo                     \
#    %{_sourcedir}/$file.desktop
#done

# Various utility directories that we want rpm to keep track of mythtv ownership
install -d $RPM_BUILD_ROOT/var/lib/mythtv
install -d $RPM_BUILD_ROOT/var/lib/cache/mythtv
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/mythtv
install -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig

# Create the plugins directory, so rpm can know mythtv owns it
install -d $RPM_BUILD_ROOT%{_libdir}/mythtv/plugins

# Install settings.pro so people can see the build options we used
install -pD settings.pro $RPM_BUILD_ROOT%{_datadir}/mythtv/build/settings.pro

%clean
rm -rf $RPM_BUILD_ROOT

%pre backend
%groupadd -g %{gid} %{name}
%useradd -u %{uid} -d /usr/share/empty -g %{name} -c "Mythtv User" %{name}

%postun backend
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%post	-n libmyth -p /sbin/ldconfig
%postun	-n libmyth -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README* UPGRADING AUTHORS COPYING FAQ
%doc database keys.txt
%doc docs contrib configfiles

%files backend
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mythbackend
%attr(755,root,root) %{_bindir}/mythfilldatabase
%attr(755,root,root) %{_bindir}/mythjobqueue
%attr(755,mythtv,mythtv) %dir /var/lib/mythtv
%attr(755,mythtv,mythtv) %dir /var/lib/cache/mythtv
%attr(754,root,root) /etc/rc.d/init.d/mythbackend
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mythbackend
%config /etc/logrotate.d/mythbackend
%attr(755,mythtv,mythtv) %dir %{_localstatedir}/log/mythtv

%files frontend
%defattr(644,root,root,755)
%dir %{_datadir}/mythtv
%dir %{_libdir}/mythtv
%{_datadir}/mythtv/*.xml
%attr(755,root,root) %{_bindir}/mythfrontend
%attr(755,root,root) %{_bindir}/mythtv
%attr(755,root,root) %{_bindir}/mythepg
%attr(755,root,root) %{_bindir}/mythprogfind
%attr(755,root,root) %{_bindir}/mythcommflag
%attr(755,root,root) %{_bindir}/mythtranscode
%attr(755,root,root) %{_bindir}/mythtvosd
%{_libdir}/mythtv/filters
%{_libdir}/mythtv/plugins
%{_datadir}/mythtv/*.ttf
%{_datadir}/mythtv/i18n
#%{_datadir}/applications/*myth*.desktop
#%{_datadir}/pixmaps/myth*.png

%files setup
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mythtv-setup

%files themes
%defattr(644,root,root,755)
%{_datadir}/mythtv/themes

%files -n libmyth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files -n libmyth-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%dir %{_datadir}/mythtv/build
%{_datadir}/mythtv/build/settings.pro

%files -n libmyth-static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
