# TODO
# - bconds: altivec joystick lcd
# - lcd? (app-misc/lcdproc)
# - icons for desktop entries
# - alpha, sparc, ppc arches?
#
# Specfile for MythTV
#
#  MythTV now uses a fairly intelligent cpu-detection script, so if you are
#  building an rpm by hand on the machine it will be used on, I encourage you
#  to use "--with cpu_autodetect" to let mythtv decide for you.
#
# Conditional build:
%bcond_with	cpu_autodetect	# enable CPU autodetection at compile time (sets "-march", "-mcpu" compile flags really)
%bcond_without	lirc		# lirc support
%bcond_without	alsa		# alsa support
%bcond_without	oss		# oss support
%bcond_without	arts		# arts support
%bcond_without	jack		# jack audio connection kit
%bcond_with	oggvorbis	# ogg vorbis (gone?!)
%bcond_without	opengl		# opengl vsync
%bcond_without	dvb		# DVB support
%bcond_without	xrandr		# disable X11 resolution switching
%bcond_with	ivtv		# ivtv support (PVR-250, PVR-350) NFY
%bcond_with	firewire	# ieee1394 (NFY)
%bcond_without	xvmc		# do not use XvMCW
%bcond_with	mmx			# enable mmx

# enable mmx automatically on arches having it
%ifarch %{ix86} %{x8664}
%ifnarch i386 i486 i586 i686
%define	with_mmx 1
%endif
%endif

Summary:	A personal video recorder (PVR) application
Summary(pl):	Osobista aplikacja do nagrywania obrazu (PVR)
Name:		mythtv
%define	_snap 20051221
%define	_rev 8332
%define	_rel 4
Version:	0.19.0.%{_snap}
Release:	1.%{_rev}.%{_rel}
License:	GPL v2
Group:		Applications/Multimedia
#Source0:	http://www.mythtv.org/mc/%{name}-%{version}.tar.bz2
Source0:	%{name}-%{_snap}.%{_rev}.tar.bz2
# Source0-md5:	aae71621a4d3a54b06ee144ce7ec2900
Source1:	mythbackend.sysconfig
Source2:	mythbackend.init
Source3:	mythbackend.logrotate
Source5:	mythfrontend.desktop
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-x86_64-configure.patch
URL:		http://www.mythtv.org/
BuildRequires:	XFree86-devel
#BuildRequires:	DirectFB-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{?with_arts:BuildRequires:	arts-devel >= 13:0.9.5}
%{?with_dvb:BuildRequires:	libdvb-devel}
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
%{?with_oggvorbis:BuildRequires:	libvorbis-devel}
%if %{with firewire}
BuildRequires:	libraw1394-devel
BuildRequires:	libavc1394-devel
BuildRequires:	libiec61883-devel # missing in PLD?
%endif
BuildRequires:	freetype-devel >= 1:2.0.0
BuildRequires:	gcc-c++
BuildRequires:	lame-libs-devel
%{?with_xvmc:BuildRequires:	libXvMCW-devel}
BuildRequires:	linux-libc-headers >= 7:2.6.10
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	mysql-devel
BuildRequires:	qmake >= 6:3.2.1-4
BuildRequires:	qt-devel >= 6:3.2.1-4
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
# for bundled libavcodec
BuildRequires:	libdts-devel
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires(post,preun):	/sbin/chkconfig
Requires:	mythtv = %{version}-%{release}
Provides:	user(mythtv)
Provides:	group(mythtv)

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
%setup -q %{?_rev:-n %{name}}
%if %{_lib} != "lib"
%patch0 -p1
%endif
%patch1 -p1

rm -rf database/old # not supported in PLD

# lib64 fix - enable to update patch
%if %{_lib} != "lib" && 0
find '(' -name '*.[ch]' -o -name '*.cpp' -o -name '*.pro' ')' | \
xargs grep -l /lib . | xargs sed -i -e '
	s,/''usr/lib/,/%{_libdir}/,g
	s,/''lib/mythtv,/%{_lib}/mythtv,g
	s,{PREFIX}/lib$,{PREFIX}/%{_lib},g
'
exit 1
%endif

%build
%if %{with cpu_autodetect}
# Make sure we have /proc mounted
if [ ! -r /proc/cpuinfo ]; then
	echo "You need to have /proc mounted in order to build with cpu_autodetect!"
	exit 1
fi
%endif
export QTDIR="%{_prefix}"

%if "%{_lib}" != "lib"
export QMAKE_LIBDIR_X11=%{_prefix}/X11R6/%{_lib}
# help configure::has_library() to locate libs
export LD_LIBRARY_PATH=%{_libdir}
%endif

# NB: not autoconf configure
export CC="%{__cc}"
export CXX="%{__cxx}"
./configure \
 	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--disable-distcc --disable-ccache \
	--compile-type=%{?debug:debug}%{!?debug:release} \
	--extra-cflags="%{rpmcflags} -fomit-frame-pointer" \
	--extra-cxxflags="%{rpmcxxflags} -fomit-frame-pointer" \
%if %{with cpu_autodetect}
	--enable-proc-opt \
%else
    %ifarch %{ix86}
		%ifarch athlon
			--arch=athlon \
		%else
			--cpu=i386 --tune=pentium4 \
		%endif
    %endif
    %ifarch %{x8664}
	--arch=x86_64 \
    %endif
	%{?with_mmx:--enable-mmx} \
%endif
	%{?with_dvb:--enable-dvb --dvb-path=%{_includedir} --enable-dvb-eit} \
	--%{?with_arts:en}%{!?with_arts:dis}able-audio-arts \
	--%{?with_alsa:en}%{!?with_alsa:dis}able-audio-alsa \
	--%{?with_oss:en}%{!?with_oss:dis}able-audio-oss \
	--%{?with_oss:en}%{!?with_oss:dis}able-audio-jack \
	--%{?with_opengl:en}%{!?with_opengl:dis}able-opengl-vsync \
	--%{?with_lirc:en}%{!?with_lirc:dis}able-lirc \
	--%{?with_firewire:en}%{!?with_firewire:dis}able-firewire \
	--%{?with_xrandr:en}%{!?with_xrandr:dis}able-xrandr \
	--%{?with_xvmc:en}%{!?with_xvmc:dis}able-xvmc \
	--enable-xv \
	--enable-x11 \

#	--%{?with_oggvorbis:en}%{!?with_oggvorbis:dis}able-vorbis \
#	--disable-joystick-menu \
#	--disable-ivtv \
#	--enable-directfb	enable DirectFB (Linux non-X11 video)
#	--enable-directx	enable DirectX  (Microsoft video)

qmake mythtv.pro
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,sysconfig} \
		$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_desktopdir}} \
		$RPM_BUILD_ROOT/var/{cache,lib,log,run}/mythtv \
		$RPM_BUILD_ROOT%{_libdir}/mythtv/plugins

export QTDIR="%{_prefix}"
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the files that we added on top of mythtv's own stuff
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/mythbackend
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/mythbackend
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/mythbackend

# desktop entries
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}

# Install settings.pro so people can see the build options we used
install -d $RPM_BUILD_ROOT%{_datadir}/mythtv/build
install config.mak settings.pro $RPM_BUILD_ROOT%{_datadir}/mythtv/build

%clean
rm -rf $RPM_BUILD_ROOT

%pre backend
%groupadd -g 149 %{name}
%useradd -u 149 -d /var/lib/mythtv -g %{name} -c "MythTV User" %{name}
%addusertogroup %{name} video
%addusertogroup %{name} audio

%post backend
/sbin/chkconfig --add mythbackend

%preun backend
if [ "$1" = "0" ]; then
	%service -q mythbackend stop
	/sbin/chkconfig --del mythbackend
fi

%postun backend
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%post	-n libmyth -p /sbin/ldconfig
%postun	-n libmyth -p /sbin/ldconfig

%post setup
if [ "$1" = 1 ]; then
%banner -e %{name}-setup <<EOF
To grant mysql permissions to mythtv, please run
zcat %{_docdir}/%{name}-setup-%{version}/database/mc.sql.gz | mysql
EOF
fi

%files
%defattr(644,root,root,755)
%doc README* UPGRADING AUTHORS FAQ
%doc docs contrib configfiles

%files backend
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mythbackend
%attr(755,root,root) %{_bindir}/mythcommflag
%attr(755,root,root) %{_bindir}/mythfilldatabase
%attr(755,root,root) %{_bindir}/mythjobqueue
%attr(755,root,root) %{_bindir}/mythlcdserver
%attr(755,root,root) %{_bindir}/mythshutdown
%attr(755,root,root) %{_bindir}/mythtranscode
%attr(755,root,root) %{_bindir}/mythwelcome
%attr(775,root,mythtv) %dir /var/lib/mythtv
%attr(775,root,mythtv) %dir /var/cache/mythtv
%attr(775,root,mythtv) %dir /var/run/mythtv
%attr(754,root,root) /etc/rc.d/init.d/mythbackend
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mythbackend
%config /etc/logrotate.d/mythbackend
%attr(775,root,mythtv) %dir %{_localstatedir}/log/mythtv

%files frontend
%defattr(644,root,root,755)
%doc keys.txt
%dir %{_datadir}/mythtv
%dir %{_libdir}/mythtv
%{_datadir}/mythtv/*.xml
%attr(755,root,root) %{_bindir}/mythfrontend
%attr(755,root,root) %{_bindir}/mythtv
#%attr(755,root,root) %{_bindir}/mythepg
#%attr(755,root,root) %{_bindir}/mythprogfind
%attr(755,root,root) %{_bindir}/mythtvosd
%dir %{_libdir}/mythtv/filters
%dir %{_libdir}/mythtv/plugins
%attr(755,root,root) %{_libdir}/mythtv/filters/*.so
%{_datadir}/mythtv/*.ttf
%{_datadir}/mythtv/i18n
%{_desktopdir}/*.desktop

%files setup
%defattr(644,root,root,755)
%doc database
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
%{_datadir}/mythtv/build

%files -n libmyth-static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
