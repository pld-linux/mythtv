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
%define with_lirc          %{?_without_lirc: 0}%{!?_without_lirc: 1}
%define with_alsa          %{?_without_alsa: 0}%{!?_without_alsa: 1}
%define with_oss           %{?_without_oss: 0}%{!?_without_oss: 1}
%define with_opengl_vsync  %{?_with_opengl_vsync: 1}%{!?_with_opengl_vsync: 0}
%define with_arts          %{?_with_arts: 1}%{!?_with_arts: 0}
%define with_xvmc          %{?_with_xvmc: 1}%{!?_with_xvmc: 0}

Name:           mythtv
Version: 0.18
Release: 0.20050326.snapshot
Summary:        A personal video recorder (PVR) application.

Group:          Applications/Multimedia
License:        GPL2
URL:            http://www.mythtv.org/

Source0:        %{name}-%{version}.tar.bz2
Source1:        mythbackend.sysconfig.in
Source2:        mythbackend.init.in
Source3:        mythbackend.logrotate.in
Source12:       http://linuxtv.org/download/dvb/%{linuxtv_dvb_package}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch:  i386 i686 athlon x86_64

BuildRequires:  gcc-c++
BuildRequires:  XFree86-devel
BuildRequires:  freetype-devel >= 2
BuildRequires:  lame-devel
BuildRequires:  qt-devel >= 3
BuildRequires:  mysql-devel
BuildRequires:  desktop-file-utils

%if %{with_alsa}
BuildRequires:  alsa-lib-devel
%endif

%if %{with_lirc}
BuildRequires:  lirc-lib-devel
%endif

%if %{with_arts}
BuildRequires:  arts-devel
%endif

%if %{with_xvmc}
BuildRequires: nvidia-graphics-devel
%endif

#%if %{with_opengl_vsync}
#BuildRequires: nvidia-graphics-devel
#%endif

%description
MythTV implements the following PVR features, and more, with a
unified graphical interface:

 - Basic 'live-tv' functionality. Pause/Fast Forward/Rewind "live" TV.
 - Video compression using RTjpeg or MPEG-4
 - Program listing retrieval using XMLTV
 - Themable, semi-transparent on-screen display
 - Electronic program guide
 - Scheduled recording of TV programs
 - Resolution of conflicts between scheduled recordings
 - Basic video editing

%package -n libmyth
Summary:        Library providing mythtv support.
Group:          System Environment/Libraries
Requires:       freetype >= 2
Requires:       lame
Requires:       qt >= 3
Requires:       qt-MySQL

%description -n libmyth
Common library code for MythTV and add-on modules (development)
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

%package -n libmyth-devel
Summary:        Development files for libmyth.
Group:          Development/Libraries
Requires:       libmyth = %{version}
BuildRequires:  freetype-devel >= 2
BuildRequires:  lame-devel
BuildRequires:  qt-devel >= 3
BuildRequires:  mysql-devel
BuildRequires:  directfb-devel
%if %{with_alsa}
BuildRequires:  alsa-lib-devel
%endif
%if %{with_lirc}
BuildRequires:  lirc-lib-devel
%endif
%if %{with_arts}
BuildRequires:  arts-devel
%endif

%description -n libmyth-devel
This package contains the header files and libraries for developing
add-ons for mythtv.

%package themes
Summary:        Base themes for mythtv's frontend.
Group:          Applications/Multimedia
Obsoletes:      mythtv-theme-Titivillus

%description themes
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the base themes used by the frontend and
mythtvsetup.

%package frontend
Summary:        Client component of mythtv (a PVR).
Group:          Applications/Multimedia
Requires:       mythtv = %{version}
Requires:       mythtv-themes = %{version}
Provides:       mythtv-frontend-api = %(echo %{version} | awk -F. '{print $1 "." $2}')

%description frontend
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the client software, which provides a
front-end for playback and configuration.  It requires access to a
mythtv-backend installation, either on the same system or one
reachable via the network.

%package backend
Summary:        Server component of mythtv (a PVR).
Group: A        pplications/Multimedia
Conflicts:      xmltv-grabbers < 0.5.34
Requires:       mythtv = %{version}

%description backend
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the server software, which provides video
and audio capture and encoding services.  In order to be useful, it
requires a mythtv-frontend installation, either on the same system or
one reachable via the network.

%package setup
Summary:        Setup the mythtv backend.
Group:          Applications/Multimedia
Requires:       mythtv-backend = %{version}
Requires:       mythtv-themes = %{version}
Provides:       mythtvsetup

%description setup
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the setup software for configuring the
mythtv backend.

%prep
%setup -q -a 12

# Install these files that MythTV doesn't include,
# and update them with the paths set by rpmbuild.
cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} .
for file in mythbackend.init \
            mythbackend.sysconfig \
            mythbackend.logrotate; do
  sed -e's|@logdir@|%{_logdir}|g' \
      -e's|@rundir@|%{_rundir}|g' \
      -e's|@sysconfigdir@|%{_sysconfigdir}|g' \
      -e's|@initdir@|%{_initdir}|g' \
      -e's|@bindir@|%{_bindir}|g' \
      -e's|@sbindir@|%{_sbindir}|g' \
      -e's|@subsysdir@|%{_subsysdir}|g' \
      -e's|@varlibdir@|%{_varlibdir}|g' \
      -e's|@varcachedir@|%{_varcachedir}|g' \
      -e's|@logrotatedir@|%{_logrotatedir}|g' \
  < $file.in > $file
done

%build
[ -n "$QTDIR" ] || . %{_sysconfdir}/profile.d/qt.sh

# Initialize the options string
OPTS=""

# Tune for the various processor types?
%if %{?_with_cpu_autodetect:0}%{!?_with_cpu_autodetect:1}
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
%if %{with_arts}
    OPTS="$OPTS --enable-audio-arts"
%else
    OPTS="$OPTS --disable-audio-arts"
%endif

# Enable alsa support (or make sure it's disabled)
%if %{with_alsa}
    OPTS="$OPTS --enable-audio-alsa"
%else
    OPTS="$OPTS --disable-audio-alsa"
%endif

# Enable oss support (or make sure it's disabled)
%if %{with_oss}
    OPTS="$OPTS --enable-audio-oss"
%else
    OPTS="$OPTS --disable-audio-oss"
%endif

# Enable xvmc support (or make sure it's disabled)
%if %{with_xvmc}
    OPTS="$OPTS --enable-xvmc --enable-xvmc-vld"
%else
    OPTS="$OPTS --disable-xvmc --disable-xvmc-vld"
%endif

# Enable opengl-vsync support (or make sure it's disabled)
%if %{with_opengl_vsync}
    OPTS="$OPTS --enable-opengl-vsync"
%else
    OPTS="$OPTS --disable-opengl-vsync"
%endif

# Enable lirc support (or make sure it's disabled)
%if %{with_lirc}
    OPTS="$OPTS --enable-lirc"
%else
    OPTS="$OPTS --disable-lirc"
%endif


# Finally, actually configure

%configure \
    --prefix=%{_prefix}            \
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
make %{?_smp_mflags}

# We don't want rpm to add perl requirements to anything in contrib
find contrib -type f | xargs -r chmod a-x

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the files that we added on top of mythtv's own stuff
install -pD mythbackend.init       $RPM_BUILD_ROOT%{_initdir}/mythbackend
install -pD mythbackend.sysconfig  $RPM_BUILD_ROOT%{_sysconfigdir}/mythbackend
install -pD mythbackend.logrotate  $RPM_BUILD_ROOT%{_logrotatedir}/mythbackend

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
mkdir -p $RPM_BUILD_ROOT%{_varlibdir}/mythtv
mkdir -p $RPM_BUILD_ROOT%{_varcachedir}/mythtv
mkdir -p $RPM_BUILD_ROOT%{_logdir}/mythtv
mkdir -p $RPM_BUILD_ROOT%{_logrotatedir}
mkdir -p $RPM_BUILD_ROOT%{_initdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfigdir}

# Create the plugins directory, so rpm can know mythtv owns it
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mythtv/plugins

# Install settings.pro so people can see the build options we used
install -pD settings.pro $RPM_BUILD_ROOT%{_datadir}/mythtv/build/settings.pro

%clean
rm -rf $RPM_BUILD_ROOT

# ldconfig's for packages that install %{_libdir}/*.so.*
# -> Don't forget Requires(post) and Requires(postun): /sbin/ldconfig
# ...and install-info's for ones that install %{_infodir}/*.info*
# -> Don't forget Requires(post) and Requires(preun): /sbin/install-info

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README* UPGRADING AUTHORS COPYING FAQ
%doc database keys.txt
%doc docs contrib configfiles

%files backend
%defattr(-,root,root,-)
%{_bindir}/mythbackend
%{_bindir}/mythfilldatabase
%{_bindir}/mythjobqueue
%attr(-,mythtv,mythtv) %dir %{_varlibdir}/mythtv
%attr(-,mythtv,mythtv) %dir %{_varcachedir}/mythtv
%{_initdir}/mythbackend
%config %{_sysconfigdir}/mythbackend
%config %{_logrotatedir}/mythbackend
%attr(-,mythtv,mythtv) %dir %{_logdir}/mythtv

%files setup
%defattr(-,root,root,-)
%{_bindir}/mythtv-setup

%files frontend
%defattr(-,root,root,-)
%{_datadir}/mythtv/*.xml
%{_bindir}/mythfrontend
%{_bindir}/mythtv
%{_bindir}/mythepg
%{_bindir}/mythprogfind
%{_bindir}/mythcommflag
%{_bindir}/mythtranscode
%{_bindir}/mythtvosd
%{_libdir}/mythtv/filters
%{_libdir}/mythtv/plugins
%{_datadir}/mythtv/*.ttf
%{_datadir}/mythtv/i18n
#%{_datadir}/applications/*myth*.desktop
#%{_datadir}/pixmaps/myth*.png

%files themes
%defattr(-,root,root,-)
%{_datadir}/mythtv/themes

%files -n libmyth
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n libmyth-devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datadir}/mythtv/build/settings.pro


%changelog

* Sat Mar 26 2005 Chris Petersen <rpm@forevermore.net> - 0.18-0.20050326.snapshot
- Finished first revision of new specfile according to new Fedora guidelines.
- Some portions of this file are based on Axel Thimm's mythtv spec, which was
- made incompatible by updates to mythtv's build process.
