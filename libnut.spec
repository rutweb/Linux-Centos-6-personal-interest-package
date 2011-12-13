# el6

%define svnrev 673

Summary: NUT Open Container Format
Name: libnut
Version: 0.0
Release: 1%{?dist}
License: BSD
Group: System Environment/Libraries
URL: http://ffmpeg.org/~michael/nut.txt

Source: %{name}-svn-r%{svnrev}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Provides: libnut = %{version}-%{release}

%description
NUT is a free multimedia container format for storage of audio, video,
subtitles and related user defined streams, it provides exact timestamps for
synchronization and seeking, is simple, has low overhead and can recover
in case of errors in the stream.

%package devel
Summary: libnut development files
Group: Development/Libraries
Provides: libnut-devel = %{version}-%{release}
Requires: %{name} = %{version}

%description devel
libnut development files.

%package utils
Group: Applications/Multimedia
Summary: libnut utils
Provides: libnut-utils = %version-%release

%description utils
This package includes libnut encoder utils.


%prep
%setup


%build
export CFLAGS='%{optflags}'
%{__make} %{?_smp_mflags} PREFIX=%{_prefix} libdir=%{_libdir}


%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} libdir=%{_libdir} install install-libnut-shared


%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_libdir}/*.so

%files utils
%{_bindir}/*

%files devel
%defattr(-, root, root, 0755)
%doc README
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Thu Dec 13 2011 nawawi jamili <nawawi@rutweb.com>
- Initial rutweb version
