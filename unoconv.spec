# el6

Summary: Tool to convert between any document format supported by OpenOffice
Name: unoconv
Version: 0.4
Release: 1%{?dist}
License: GPL
Group: System Environment/Base
URL: http://dag.wieers.com/home-made/unoconv/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dag.wieers.com/home-made/unoconv/unoconv-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: python >= 2.0
Requires: python >= 2.0

%description
unoconv converts between any document format that OpenOffice understands.
It uses OpenOffice's UNO bindings for non-interactive conversion of
documents.

Supported document formats include Open Document Format (.odf),
MS Word (.doc), MS Office Open/MS OOXML (.xml),
Portable Document Format (.pdf), HTML, XHTML, RTF, Docbook (.xml),
and more.

%prep
%setup

%build

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING README TODO WISHLIST docs/ tests/
%doc %{_mandir}/man1/unoconv.1*
%{_bindir}/unoconv

%changelog
* Thu Dec 13 2011 nawawi jamili <nawawi@rutweb.com>
- Initial rutweb version
