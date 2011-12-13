# el6

Summary: Library for decoding ATSC A/52 (aka AC-3) audio streams
Name: a52dec
Version: 0.7.4
Release: 8%{?dist}
License: GPL
Group: Applications/Multimedia
URL: http://liba52.sourceforge.net/

Source: http://liba52.sourceforge.net/files/a52dec-%{version}.tar.gz
Patch0: a52dec-0.7.4-PIC.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++
BuildRequires: autoconf >= 2.52, automake, libtool

%description
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.


%package devel
Summary: Development header files and static library for liba52
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.

These are the header files and static libraries from liba52 that are needed
to build programs that use it.


%prep
%setup
%patch0 -p1 -b .PIC


%build
%{__libtoolize} --force
%{__aclocal}
%{__automake} -a
%{__autoconf}
%configure --enable-shared
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING doc/liba52.txt HISTORY NEWS README TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*


%files devel
%defattr(-, root, root, 0755)
%{_includedir}/*
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Thu Dec 13 2011 nawawi jamili <nawawi@rutweb.com>
- Initial rutweb version

