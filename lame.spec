# el6

Summary: LAME Ain't an MP3 Encoder... but it's the best of all
Name: lame
Version: 3.99
Release: 1%{?dist}
License: LGPL
Group: Applications/Multimedia
URL: http://lame.sourceforge.net/

Source: http://dl.sf.net/project/lame/lame/%{version}/lame-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++
BuildRequires: gtk2-devel
BuildRequires: libtool
BuildRequires: libvorbis-devel
BuildRequires: ncurses-devel
%{?!_without_selinux:BuildRequires: prelink}
%ifarch %{ix86} x86_64
BuildRequires: nasm
%endif
Provides: mp3encoder

%description
LAME is an educational tool to be used for learning about MP3 encoding.  The
goal of the LAME project is to use the open source model to improve the
psychoacoustics, noise shaping and speed of MP3. Another goal of the LAME
project is to use these improvements for the basis of a patent-free audio
compression codec for the GNU project.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup

%build
%configure \
    --disable-dependency-tracking \
    --disable-static \
    --program-prefix="%{?_program_prefix}" \
%ifarch %{ix86} x86_64
    --enable-nasm \
%endif
    --enable-decoder
%{__make} test CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

### Some apps still expect to find <lame.h>
%{__ln_s} -f lame/lame.h %{buildroot}%{_includedir}/lame.h

### Clean up documentation to be included
find doc/html -name "Makefile*" | xargs rm -f
%{__rm} -rf %{buildroot}%{_docdir}/lame/

### Clear not needed executable stack flag bit
execstack -c %{buildroot}%{_libdir}/*.so.*.*.* || :

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING INSTALL* doc/html/
%doc LICENSE README TODO USAGE
%doc %{_mandir}/man1/lame.1*
%{_bindir}/lame
%{_libdir}/libmp3lame.so.*

%files devel
%defattr(-, root, root, 0755)
%doc API DEFINES HACKING STYLEGUIDE
%{_includedir}/lame/
%{_includedir}/lame.h
%{_libdir}/libmp3lame.so
%exclude %{_libdir}/libmp3lame.la

%changelog
* Thu Dec 13 2011 nawawi jamili <nawawi@rutweb.com>
- Initial rutweb version
