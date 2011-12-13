# el6

Summary:   HE-AAC+ codec as shared library
Name:      libaacplus
Version:   2.0.2
Release:   1%{?dist}
License:   3GPP
Group:     Applications/Multimedia
URL:       http://tipok.org.ua/node/17
Source0:   http://tipok.org.ua/downloads/media/aac+/libaacplus/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, libtool
BuildRequires: fftw-devel, wget

%description
HE-AAC+ v2 library, based on the 3GPP reference implementation.

%package devel
Summary:         The %{name} development files
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig

%description devel
This package contains development files for %{name}.

%prep
%setup -q

%build
./autogen.sh
%configure
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/aacplusenc
%{_libdir}/libaacplus.so.*
%{_mandir}/man1/aacplusenc.1.gz

%files devel
%defattr(-,root,root,-)
%{_libdir}/libaacplus.so
%{_libdir}/libaacplus.a
%{_libdir}/libaacplus.la
%{_includedir}/aacplus.h
%{_libdir}/pkgconfig/aacplus.pc

%changelog
* Thu Dec 13 2011 nawawi jamili <nawawi@rutweb.com>
- Initial rutweb version
