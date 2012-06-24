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

%define		qtver	4.3
%define		snap	20081007

Summary:	A personal video recorder (PVR) application
Summary(pl.UTF-8):	Osobista aplikacja do nagrywania obrazu (PVR)
Name:		mythtv
Version:	0.22
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/Multimedia
Source0:	%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	5a10a4752a950c246859c2a2710d2f47
Source1:	mythbackend.sysconfig
Source2:	mythbackend.init
Source3:	mythbackend.logrotate
Source5:	mythfrontend.desktop
Patch0:		%{name}-configure.patch
URL:		http://www.mythtv.org/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	QtCore-devel >= %{qtver}
BuildRequires:	QtGui-devel >= %{qtver}
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtOpenGL-devel >= %{qtver}
BuildRequires:	QtSql-devel >= %{qtver}
BuildRequires:	QtWebKit-devel >= %{qtver}
BuildRequires:	QtXml-devel >= %{qtver}
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	ffmpeg-devel
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	lame-libs-devel
%{?with_xvmc:BuildRequires:	xorg-lib-libXvMC-devel}
%{?with_firewire:BuildRequires:	libavc1394-devel}
%{?with_dvb:BuildRequires:	libdvb-devel}
BuildRequires:	libdvdnav-devel
%{?with_firewire:BuildRequires:	libiec61883-devel}
%{?with_firewire:BuildRequires:	libraw1394-devel}
BuildRequires:	linux-libc-headers >= 7:2.6.10
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	mysql-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
# for bundled libavcodec
BuildRequires:	libdts-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	myth_api_version %(echo %{version} | cut -d. -f1,2)

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

%description -l pl.UTF-8
MythTV implementuje następujące możliwości PVR, a nawet więcej, wraz z
ujednoliconym interfejsem graficznym:
- podstawowa funkcjonalność "live-tv"; pauza, szybkie przewijanie,
  przewijanie "żywej" telewizji
- kompresja obrazu przy użyciu RTjpeg lub MPEG-4
- odczyt listy programów przy użyciu XMLTV
- pseudoprzezroczyste wyświetlanie na obrazie (OSD) z obsługą motywów
- elektroniczny przewodnik po programie
- planowane nagrywanie programów telewizyjnych
- rozwiązywanie konfliktów między planowanymi nagraniami
- podstawowa edycja obrazu

%package backend
Summary:	Server component of mythtv (a PVR)
Summary(pl.UTF-8):	Część serwerowa mythtv (PVR)
Group:		Applications/Multimedia
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	libmyth = %{version}-%{release}
Requires:	mythtv = %{version}-%{release}
Provides:	group(mythtv)
Provides:	user(mythtv)

%description backend
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the server software, which provides video
and audio capture and encoding services. In order to be useful, it
requires a mythtv-frontend installation, either on the same system or
one reachable via the network.

%description backend -l pl.UTF-8
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
oglądania programów telewizyjnych. Więcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko oprogramowanie serwerowe, udostępniające
usługi przechwytywania i kodowania obrazu i dźwięku. Aby było
przydatne, wymaga instalacji mythtv-frontend - na tym samym systemie,
albo innym osiągalnym po sieci.

%package frontend
Summary:	Client component of mythtv (a PVR)
Summary(pl.UTF-8):	Część kliencka mythtv (PVR)
Group:		Applications/Multimedia
Requires:	libmyth = %{version}-%{release}
Requires:	mythtv = %{version}-%{release}
Requires:	mythtv-themes = %{version}-%{release}
Provides:	mythtv-frontend-api = %{myth_api_version}

%description frontend
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the client software, which provides a
front-end for playback and configuration. It requires access to a
mythtv-backend installation, either on the same system or one
reachable via the network.

%description frontend -l pl.UTF-8
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
oglądania programów telewizyjnych. Więcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko oprogramowanie klienckie, dostarczające
frontend do odtwarzania i konfiguracji. Wymaga dostępu do instalacji
mythtv-backend - na tym samym systemie, albo innym osiągalnym po
sieci.

%package setup
Summary:	Setup the mythtv backend
Summary(pl.UTF-8):	Konfigurator backendu mythtv
Group:		Applications/Multimedia
Requires:	libmyth = %{version}-%{release}

%description setup
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the setup software for configuring the
mythtv backend.

%description setup -l pl.UTF-8
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
oglądania programów telewizyjnych. Więcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko program do konfigurowania backendu mythtv.

%package themes
Summary:	Base themes for mythtv's frontend
Summary(pl.UTF-8):	Podstawowe motywy dla frontendu mythtv
Requires:	%{name}-frontend = %{version}-%{release}
Group:		Themes

%description themes
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the base themes used by the frontend and
mythtvsetup.

%description themes -l pl.UTF-8
MythTV dostarcza ujednolicony interfejs graficzny do nagrywania i
oglądania programów telewizyjnych. Więcej informacji w pakiecie
mythtv.

Ten pakiet zawiera tylko podstawowe motywy używane przez frontend oraz
mythtvsetup.

%package -n libmyth
Summary:	Library providing mythtv support
Summary(pl.UTF-8):	Biblioteka udostępniająca obsługę mythtv
Group:		Libraries
Requires:	freetype >= 1:2.0.0
Requires:	lame
Requires:	qt >= 6:3.2.1-4
Requires:	qt-plugin-mysql >= 6:3.2.1-4

%description -n libmyth
Common library code for MythTV and add-on modules (development) MythTV
provides a unified graphical interface for recording and viewing
television programs. Refer to the mythtv package for more information.

%description -n libmyth -l pl.UTF-8
Wspólny kod biblioteki dla MythTV i dodatkowych modułów MythTV
dostarczający ujednolicony interfejs graficzny do nagrywania i
oglądania programów telewizyjnych. Więcej informacji w pakiecie
mythtv.

%package -n libmyth-devel
Summary:	Development files for libmyth
Summary(pl.UTF-8):	Pliki nagłówkowe libmyth
Group:		Development/Libraries
Requires:	libmyth = %{version}-%{release}

%description -n libmyth-devel
This package contains the header files for developing add-ons for
mythtv.

%description -n libmyth-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia dodatków dla mythtv.

%package -n libmyth-static
Summary:	Static libmyth library
Summary(pl.UTF-8):	Statyczna biblioteka libmyth
Group:		Development/Libraries
Requires:	libmyth-devel = %{version}-%{release}

%description -n libmyth-static
Static libmyth library.

%description -n libmyth-static -l pl.UTF-8
Statyczna biblioteka libmyth.

%prep
%setup -q -n %{name}-%{version}-%{snap}
%patch0 -p0

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

# NB: not autoconf configure
# help configure::has_library() to locate libs
LD_LIBRARY_PATH=%{_libdir} \
CC="%{__cc}" \
CXX="%{__cxx}" \
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
	%{?with_dvb:--enable-dvb --dvb-path=%{_includedir}} \
	--%{?with_arts:en}%{!?with_arts:dis}able-audio-arts \
	--%{?with_alsa:en}%{!?with_alsa:dis}able-audio-alsa \
	--%{?with_oss:en}%{!?with_oss:dis}able-audio-oss \
	--%{?with_jack:en}%{!?with_jack:dis}able-audio-jack \
	--%{?with_opengl:en}%{!?with_opengl:dis}able-opengl-vsync \
	--%{?with_lirc:en}%{!?with_lirc:dis}able-lirc \
	--%{?with_firewire:en}%{!?with_firewire:dis}able-firewire \
	--%{?with_xrandr:en}%{!?with_xrandr:dis}able-xrandr \
	--%{?with_xvmc:en}%{!?with_xvmc:dis}able-xvmc \
	--enable-xv \
	--enable-x11 \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,sysconfig} \
		$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_desktopdir}} \
		$RPM_BUILD_ROOT/var/{cache,lib,log,run}/mythtv \
		$RPM_BUILD_ROOT%{_libdir}/mythtv/plugins

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

for p in mythfrontend; do
	for l in $RPM_BUILD_ROOT%{_datadir}/mythtv/i18n/${p}_*.qm; do
		echo $l | sed -e "s,^$RPM_BUILD_ROOT\(.*${p}_\(.*\).qm\),%%lang(\2) \1,"
	done > $p.lang
done

# glibc language codes. attempt was made to change it on libmyth side,
# but that was just asking for trouble due large coverage of
# language.lower() usage.
sed -i -e '
s,%%lang(en_gb),%%lang(en_GB),
s,%%lang(zh_tw),%%lang(zh_TW),
s,%%lang(pt_br),%%lang(pt_BR),
' *.lang

rm -rf mythtvosd mythwelcome mythlcdserver
install -d mythtvosd mythwelcome
cp -a programs/mythtvosd/{README,*.xml} mythtvosd
cp -a programs/mythwelcome/README mythwelcome
cp -a programs/mythlcdserver/README mythlcdserver

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
#%doc docs contrib configfiles
%doc keys.txt mythtvosd mythwelcome mythlcdserver

%files backend
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mythbackend
%attr(755,root,root) %{_bindir}/mythcommflag
%attr(755,root,root) %{_bindir}/mythfilldatabase
%attr(755,root,root) %{_bindir}/mythjobqueue
%attr(755,root,root) %{_bindir}/mythlcdserver
%attr(755,root,root) %{_bindir}/mythtranscode
%attr(755,root,root) %{_bindir}/mythreplex
%attr(775,root,mythtv) %dir /var/lib/mythtv
%attr(775,root,mythtv) %dir /var/cache/mythtv
%attr(775,root,mythtv) %dir /var/run/mythtv
%attr(754,root,root) /etc/rc.d/init.d/mythbackend
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mythbackend
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mythbackend
%attr(775,root,mythtv) %dir %{_localstatedir}/log/mythtv

%files frontend -f mythfrontend.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mythfrontend
%attr(755,root,root) %{_bindir}/mythshutdown
%attr(755,root,root) %{_bindir}/mythtv
%attr(755,root,root) %{_bindir}/mythtvosd
%attr(755,root,root) %{_bindir}/mythwelcome
%dir %{_datadir}/mythtv
%dir %{_datadir}/mythtv/themes
%dir %{_libdir}/mythtv
%{_datadir}/mythtv/*.xml
%dir %{_libdir}/mythtv/filters
%dir %{_libdir}/mythtv/plugins
%attr(755,root,root) %{_libdir}/mythtv/filters/*.so
%{_datadir}/mythtv/*.ttf
%dir %{_datadir}/mythtv/i18n
%{_desktopdir}/*.desktop

%files setup
%defattr(644,root,root,755)
%doc database
%attr(755,root,root) %{_bindir}/mythtv-setup

%files themes
%defattr(644,root,root,755)
%{_datadir}/mythtv/themes/*

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
