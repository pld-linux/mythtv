# TODO
# - bconds: altivec joystick lcd
# - lcd? (app-misc/lcdproc)
# - alpha, sparc, ppc arches?
# - http://outflux.net/software/pkgs/mythtvfs-fuse/
# - vaapi support - check for compatible versions of libva?
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
%bcond_without	jack		# jack audio connection kit
%bcond_without  pulseaudio	# pulseaudio support
%bcond_without	opengl		# opengl vsync
%bcond_without	dvb		# DVB support
%bcond_without	xrandr		# disable X11 resolution switching
%bcond_without	ivtv		# ivtv support (PVR-250, PVR-350) NFY
%bcond_without	iptv
%bcond_without	firewire	# ieee1394 (NFY)
%bcond_without	xvmc		# do not use XvMCW
%bcond_without  vdpau		# disable nvidia vdpau support
%bcond_without  fftw3		# disable fftw3 support
%bcond_with	mmx		# enable MMX
%bcond_without	nellymoserdec
%bcond_with	vaapi		# enable vaapi
%bcond_with     dshowserver	# enable directshow codecs server
%bcond_with 	directfb
%bcond_with	nvidia_headers	# build vdpau support with nvidia headers 
				# instead of libvdpau

# enable mmx automatically on arches having it
%ifarch %{ix86} %{x8664}
%ifnarch i386 i486 i586 i686
%define	with_mmx 1
%endif
%endif

# dshowserver is exclusive arch for x86 x86_64 only
%ifnarch %{ix86} %{x8664}
%undefine with_dshowserver
%endif

Summary:	A personal video recorder (PVR) application
Summary(pl.UTF-8):	Osobista aplikacja do nagrywania obrazu (PVR)
Name:		mythtv
Version:	0.23.1
Release:	4
License:	GPL v2
Group:		Applications/Multimedia
Source0:	ftp://ftp.osuosl.org/pub/mythtv/%{name}-%{version}.tar.bz2
# Source0-md5:	3379a5fd12ae866cd10c5b5d23439898
Source1:	mythbackend.sysconfig
Source2:	mythbackend.init
Source3:	mythbackend.logrotate
Source5:	pld-mythfrontend.desktop
# Source5-md5:	f37a903ac97463683bebacdf29406951
Source6:	pld-mythfrontend.png
# Source6-md5:	bf76bd1463a022e174e4af976a03e678
Source20:	dshowcodecs
# Source20-md5:	48327772b9e150f69e1ab8ff44b9a76c
Patch0:		%{name}-configure.patch
Patch10:	%{name}-sbinpath.patch
Patch20:	%{name}-compile_fixes_for_qt_4_7.patch
Patch30:	%{name}-dshowserver-0.22.patch
URL:		http://www.mythtv.org/
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	Qt3Support-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtOpenGL-devel
BuildRequires:	QtScript-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	QtXml-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	ffmpeg-devel
%{?with_fftw3:BuildRequires: fftw3-devel,fftw3-single-devel}
BuildRequires:	freetype-devel >= 1:2.0.0
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	lame-libs-devel
%{?with_firewire:BuildRequires:	libavc1394-devel}
BuildRequires:	libdts-devel
%{?with_dvb:BuildRequires:	libdvb-devel}
BuildRequires:	libdvdnav-devel
%{?with_firewire:BuildRequires:	libiec61883-devel}
%{?with_firewire:BuildRequires:	libraw1394-devel}
%{!?with_nvidia_headers:%{?with_vdpau:BuildRequires:	libvdpau-devel}}
BuildRequires:	linux-libc-headers >= 7:2.6.10
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	mysql-devel
BuildRequires:	perl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires: pulseaudio-devel}
BuildRequires:	python-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	which
%{?with_nvidia_headers:%{?with_vdpau:BuildRequires: xorg-driver-video-nvidia-devel}}
BuildRequires:	xorg-lib-libXext-devel
%{?with_xvmc:BuildRequires:	xorg-lib-libXvMC-devel}
BuildRequires:	xorg-lib-libXxf86vm-devel
%{!?with_pulseaudio:BuildConflicts: pulseaudio-devel}
%{!?with_nvidia_headers:BuildConflicts:	xorg-driver-video-nvidia-devel}
# for Perl bindings
BuildRequires:	perl-ExtUtils-MakeMaker
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
Suggests:	mysql
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
albo innym osiągalnym w sieci.

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
mythtv-backend - na tym samym systemie, albo innym osiągalnym w sieci.

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
Group:		Themes
Requires:	%{name}-frontend = %{version}-%{release}

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
Requires:	QtSql-mysql
Requires:	freetype >= 1:2.0.0
Requires:	lame

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

%package -n perl-MythTV
Summary:	MythTV Perl bindings
Summary(pl.UTF-8):	Interfejs Perla dla MythTV
Group:		Libraries

%description -n perl-MythTV
MythTV Perl bindings.

%description -n perl-MythTV -l pl.UTF-8
Ten pakiet zawiera moduły Perla do tworzenia dodatków dla mythtv.

%package -n python-MythTV
Summary:	MythTV Python bindings
Summary(pl.UTF-8):	Interfejs Pythona dla MythTV
Group:		Libraries
Requires:	python-MySQLdb

%description -n python-MythTV
MythTV Python bindings.

%description -n python-MythTV -l pl.UTF-8
Ten pakiet zawiera moduły Pythona do tworzenia dodatków dla mythtv.

%prep

%setup -q

%{__sed} -i -e 's,/var/log/mythfilldatabase.log,/var/log/mythtv/mythfilldatabase.log,' \
	programs/mythbackend/housekeeper.cpp programs/mythwelcome/welcomedialog.cpp

%patch0  -p1
%patch10 -p1
%patch20 -p1
#%patch30 -p1

%{?with_dshowserver:%patch20 -p0}
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

# Assigning null to QMAKE_LIBDIR_QT will prevent makefiles contain
# -L$(QTDIR)/%{_lib} and -Wl,-rpath,$(QTDIR)/%{_lib}. And that will
# prevent compiler finding libs from system when they should be looked
# from current buildtree.
# but that made it link with -lqt which doesn't exist, instead of -lqt-mt
# so we make QMAKE wrapper which will do sed subst after calling
# qmake. this is the wrapper.
cat > qmake-wrapper.sh <<'EOF'
#!/bin/sh
getmakefile() {
	while [ $# -gt 0 ]; do
		case "$1" in
		-o)
			shift
			makefile="$1"
			return
			;;
	esac
		shift
	done
}

qmake-qt4 "$@"
getmakefile "$@"
if [ "$makefile" ]; then
	%{__sed} -i -e '
		s;-Wl,-rpath,$(QTDIR)/%{_lib};;
		s;-L$(QTDIR)/%{_lib};;
	' $makefile
fi
EOF
chmod +x qmake-wrapper.sh

# move perl bindings to vendor prefix
sed -i -e 's#perl Makefile.PL#%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"#' \
   bindings/perl/perl.pro

%build

%if %{with cpu_autodetect}
# Make sure we have /proc mounted
if [ ! -r /proc/cpuinfo ]; then
	echo "You need to have /proc mounted in order to build with cpu_autodetect!"
	exit 1
fi
%endif

./configure \
 	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libdir-name=%{_lib} \
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
			--cpu=%{_target_cpu} --tune=pentium4 \
		%endif
	%endif
	%ifarch i386 i486 i586
	--enable-disable-mmx-for-debugging \
	%endif
	%ifarch %{x8664}
	--arch=x86_64 \
	%endif
	%{?with_mmx:--enable-mmx} \
%endif
	%{?with_dvb:--enable-dvb --dvb-path=%{_includedir}} \
	--%{?with_alsa:en}%{!?with_alsa:dis}able-audio-alsa \
	--%{?with_oss:en}%{!?with_oss:dis}able-audio-oss \
	--%{?with_jack:en}%{!?with_jack:dis}able-audio-jack \
	--%{?with_opengl:en}%{!?with_opengl:dis}able-opengl-vsync \
	--%{?with_lirc:en}%{!?with_lirc:dis}able-lirc \
	--%{?with_firewire:en}%{!?with_firewire:dis}able-firewire \
	--%{?with_xrandr:en}%{!?with_xrandr:dis}able-xrandr \
	--%{?with_xvmc:en}%{!?with_xvmc:dis}able-xvmc \
	--%{?with_ivtv:en}%{!?with_ivtv:dis}able-ivtv \
	--%{?with_iptv:en}%{!?with_iptv:dis}able-iptv \
	--%{?with_nellymoserdec:en}%{!?with_nellymoserdec:dis}able-decoder=nellymoser \
	--%{?with_vaapi:en}%{!?with_vaapi:dis}able-vaapi \
	--%{?with_vdpau:en}%{!?with_vdpau:dis}able-vdpau \
	--%{?with_directfb:en}%{!?with_directfb:dis}able-directfb \
	--%{?with_fftw3:en}%{!?with_fftw3:dis}able-libfftw3 \
	--enable-xv \
	--enable-x11 \

%{_libdir}/qt4/bin/qmake mythtv.pro
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,sysconfig} \
		$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_desktopdir}} \
		$RPM_BUILD_ROOT/var/{cache,log,run}/mythtv \
		$RPM_BUILD_ROOT/var/lib/mythtv/tmp \
		$RPM_BUILD_ROOT%{_libdir}/mythtv \
		$RPM_BUILD_ROOT%{_libdir}/mythtv/plugins \
		$RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the files that we added on top of mythtv's own stuff
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/mythbackend
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/mythbackend
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/mythbackend
%{?with_dshowserver:install %{SOURCE20} $RPM_BUILD_ROOT%{_datadir}/mythtv}

# desktop entries
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE6} $RPM_BUILD_ROOT%{_pixmapsdir}

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
%doc docs contrib config
%doc keys.txt mythtvosd mythwelcome mythlcdserver

%files backend
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mythbackend
%attr(755,root,root) %{_sbindir}/mythcommflag
%attr(755,root,root) %{_bindir}/mythfilldatabase
%attr(755,root,root) %{_sbindir}/mythjobqueue
%attr(755,root,root) %{_sbindir}/mythlcdserver
%attr(755,root,root) %{_bindir}/mythtranscode
%attr(755,root,root) %{_bindir}/mythreplex
%attr(775,root,mythtv) %dir /var/lib/mythtv
%attr(700,root,mythtv) %dir /var/lib/mythtv/tmp
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
%attr(755,root,root) %{_bindir}/mythavtest
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
%if %{with dshowserver}
%{_datadir}/mythtv/dshowcodecs
%endif
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%files setup
%defattr(644,root,root,755)
%doc database
%attr(755,root,root) %{_bindir}/mythtv-setup

%files themes
%defattr(644,root,root,755)
%{_datadir}/mythtv/themes/*

%files -n libmyth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so*
%attr(755,root,root) %{_libdir}/lib*.a
%{_datadir}/mythtv/*.pl

%files -n libmyth-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/mythtv/build

%files -n libmyth-static
%defattr(644,root,root,755)

%files -n perl-MythTV
%defattr(644,root,root,755)
%{perl_vendorlib}/MythTV.pm
%dir %{perl_vendorlib}/MythTV
%{perl_vendorlib}/MythTV/*.pm
%dir %{perl_vendorlib}/IO/Socket/INET
%{perl_vendorlib}/IO/Socket/INET/MythTV.pm
%exclude %{perl_vendorarch}/auto/MythTV/.packlist

%files -n python-MythTV
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mythpython
%dir %{py_sitescriptdir}/MythTV
%{py_sitescriptdir}/MythTV/*
%{py_sitescriptdir}/*.egg-info
