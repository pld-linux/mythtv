#
# Specfile for MythTV
#
#  MythTV now uses a fairly intelligent cpu-detection script, so if you are
#  building an rpm by hand on the machine it will be used on, I encourage you
#  to use "--with cpu_autodetect" to let mythtv decide for you.
#

# The name of the DVB driver package (used in a couple of places,
# so it's not hard-coded in the spec itself)
%define linuxtv_dvb_package linuxtv-dvb-1.1.1

# Compile type:  debug or release
%define compile_type debug

# Set up some custom-build parameters
%bcond_with	lirc
%bcond_without alsa
%bcond_without oss
%bcond_with opengl_vsync
%bcond_with arts
%bcond_with xvmc
%bcond_with cpu_autodetect # enable cpu autodetection at compile time

Name:		mythtv
Version:	0.17
#define _snap 20050326
Release:	0.1
Summary:	A personal video recorder (PVR) application.
Group:		Applications/Multimedia
License:	GPL v2
URL:		http://www.mythtv.org/
Source0:	http://www.mythtv.org/mc/%{name}-%{version}.tar.bz2
# Source0-md5:	c996dc690d36e946396fc5cd4b715e3b
Source1:	mythbackend.sysconfig.in
Source2:	mythbackend.init.in
Source3:	mythbackend.logrotate.in
Source12:	http://linuxtv.org/download/dvb/%{linuxtv_dvb_package}.tar.bz2
# Source12-md5:	6dd599f24b7abecd1e32c203eaa7fa8a
ExclusiveArch:	i386 i686 athlon x86_64
BuildRequires:	gcc-c++
BuildRequires:	XFree86-devel
BuildRequires:	freetype-devel >= 1:2.0.0
BuildRequires:	lame-libs-devel
BuildRequires:	qt-devel >= 6:3.2.1-4
BuildRequires:	qmake >= 6:3.2.1-4
BuildRequires:	mysql-devel
BuildRequires:	desktop-file-utils
%if %{with alsa}
BuildRequires:	alsa-lib-devel
%endif
%if %{with lirc}
BuildRequires:	lirc-devel
%endif
%if %{with arts}
BuildRequires:	arts-devel >= 13:0.9.5
%endif
%if %{with xvmc}
BuildRequires:	nvidia-graphics-devel
%endif
#%if %{with opengl_vsync}
#BuildRequires: nvidia-graphics-devel
#%endif
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

%package -n libmyth
Summary:	Library providing mythtv support.
Group:		Libraries
Requires:	freetype >= 1:2.0.0
Requires:	lame
Requires:	qt >= 6:
Requires:	qt-plugin-mysql >= 6:3.2.1-4

%description -n libmyth
Common library code for MythTV and add-on modules (development) MythTV
provides a unified graphical interface for recording and viewing
television programs. Refer to the mythtv package for more information.

%package -n libmyth-devel
Summary:	Development files for libmyth.
Group:		Development/Libraries
Requires:	libmyth = %{version}-%{release}
BuildRequires:	freetype-devel >= 1:2.0.0
BuildRequires:	lame-libs-devel
BuildRequires:	qt-devel >= 6:3.2.1-4
BuildRequires:	mysql-devel
BuildRequires:	DirectFB-devel
%if %{with alsa}
BuildRequires:	alsa-lib-devel
%endif
%if %{with lirc}
BuildRequires:	lirc-devel
%endif
%if %{with arts}
BuildRequires:	arts-devel >= 13:0.9.5
%endif

%description -n libmyth-devel
This package contains the header files and libraries for developing
add-ons for mythtv.

%package themes
Summary:	Base themes for mythtv's frontend.
Group:		Applications/Multimedia
Obsoletes:	mythtv-theme-Titivillus

%description themes
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the base themes used by the frontend and
mythtvsetup.

%package frontend
Summary:	Client component of mythtv (a PVR).
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

%package backend
Summary:	Server component of mythtv (a PVR).
Group:		Applications/Multimedia
Conflicts:	xmltv-grabbers < 0.5.34
Requires:	mythtv = %{version}-%{release}

%description backend
MythTV provides a unified graphical interface for recording and
viewing television programs. Refer to the mythtv package for more
information.

This package contains only the server software, which provides video
and audio capture and encoding services. In order to be useful, it
requires a mythtv-frontend installation, either on the same system or
one reachable via the network.

%package setup
Summary:	Setup the mythtv backend.
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

%prep
%setup -q -a 12

# Install these files that MythTV doesn't include,
# and update them with the paths set by rpmbuild.
%if 0
cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} .
for file in mythbackend.init \
            mythbackend.sysconfig \
            mythbackend.logrotate; do
  sed -e's|@logdir@|%{_localstatedir}/log|g' \
      -e's|@rundir@|%{_rundir}|g' \
      -e's|@sysconfigdir@|%{_sysconfdir}|g' \
      -e's|@initdir@|%{_initrddir}|g' \
      -e's|@bindir@|%{_bindir}|g' \
      -e's|@sbindir@|%{_sbindir}|g' \
      -e's|@subsysdir@|%{_subsysdir}|g' \
      -e's|@varlibdir@|/var/lib|g' \
      -e's|@varcachedir@|%{_varcachedir}|g' \
      -e's|@logrotatedir@|%{_sysconfdir}/logrotate.d|g' \
  < $file.in > $file
done
%endif

%build
export QTDIR="%{_prefix}"

# Initialize the options string
OPTS=""

# Tune for the various processor types?
%if %{with cpu_autodetect}
    %ifarch i386
        OPTS="$OPTS --cpu=i386 --tune=pentium4 --enable-mmx"
    %endif
    %ifarch i686
        OPTS="$OPTS --cpu=i686 --tune=pentium4 --enable-mmx"
    %endif
    %ifarch athlon
        OPTS="$OPTS --arch=athlon"
    %endif
    %ifarch x86_64
        OPTS="$OPTS --arch=x86_64"
    %endif
%endif

# Enable arts support (or make sure it's disabled)
%if %{with arts}
    OPTS="$OPTS --enable-audio-arts"
%else
    OPTS="$OPTS --disable-audio-arts"
%endif

# Enable alsa support (or make sure it's disabled)
%if %{with alsa}
    OPTS="$OPTS --enable-audio-alsa"
%else
    OPTS="$OPTS --disable-audio-alsa"
%endif

# Enable oss support (or make sure it's disabled)
%if %{with oss}
    OPTS="$OPTS --enable-audio-oss"
%else
    OPTS="$OPTS --disable-audio-oss"
%endif

# Enable xvmc support (or make sure it's disabled)
%if %{with xvmc}
    OPTS="$OPTS --enable-xvmc --enable-xvmc-vld"
%else
    OPTS="$OPTS --disable-xvmc --disable-xvmc-vld"
%endif

# Enable opengl-vsync support (or make sure it's disabled)
%if %{with opengl_vsync}
    OPTS="$OPTS --enable-opengl-vsync"
%else
    OPTS="$OPTS --disable-opengl-vsync"
%endif

# Enable lirc support (or make sure it's disabled)
%if %{with lirc}
    OPTS="$OPTS --enable-lirc"
%else
    OPTS="$OPTS --disable-lirc"
%endif


# Finally, actually configure

%configure \
    --compile-type=%{compile_type} \
    --disable-audio-jack           \
    --enable-dvb                   \
    --dvb-path=%{_builddir}/%{name}-%{version}/%{linuxtv_dvb_package}/linux/include/ \
    $OPTS
#  --disable-joystick-menu  \
#  --disable-firewire       \
#  --disable-ivtv           \
#  --enable-dvb-eit         \

# MythTV doesn't support parallel builds
qmake mythtv.pro
%{__make} %{?_smp_mflags}

# We don't want rpm to add perl requirements to anything in contrib
find contrib -type f | xargs -r chmod a-x

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the files that we added on top of mythtv's own stuff
install -pD mythbackend.init       $RPM_BUILD_ROOT%{_initrddir}/mythbackend
install -pD mythbackend.sysconfig  $RPM_BUILD_ROOT%{_sysconfdir}/mythbackend
install -pD mythbackend.logrotate  $RPM_BUILD_ROOT/etc/logrotate.d/mythbackend

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
install -d $RPM_BUILD_ROOT%{_initrddir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}

# Create the plugins directory, so rpm can know mythtv owns it
install -d $RPM_BUILD_ROOT%{_libdir}/mythtv/plugins

# Install settings.pro so people can see the build options we used
install -pD settings.pro $RPM_BUILD_ROOT%{_datadir}/mythtv/build/settings.pro

%clean
rm -rf $RPM_BUILD_ROOT

# ldconfig's for packages that install %{_libdir}/*.so.*
# -> Don't forget Requires(post) and Requires(postun): /sbin/ldconfig
# ...and install-info's for ones that install %{_infodir}/*.info*
# -> Don't forget Requires(post) and Requires(preun): /sbin/install-info

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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
%attr(-,mythtv,mythtv) %dir /var/lib/mythtv
%attr(-,mythtv,mythtv) %dir /var/lib/cache/mythtv
%{_initrddir}/mythbackend
%config %{_sysconfdir}/mythbackend
%config /etc/logrotate.d/mythbackend
%attr(-,mythtv,mythtv) %dir %{_localstatedir}/log/mythtv

%files setup
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mythtv-setup

%files frontend
%defattr(644,root,root,755)
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

%files themes
%defattr(644,root,root,755)
%{_datadir}/mythtv/themes

%files -n libmyth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libmyth-devel
%defattr(644,root,root,755)
%{_includedir}/*
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.a
%{_datadir}/mythtv/build/settings.pro
