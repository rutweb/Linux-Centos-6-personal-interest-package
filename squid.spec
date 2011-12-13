# el6

%define __perl_requires %{SOURCE98}

Summary: The Squid proxy caching server.
Name: squid
Version: 2.7.STABLE9
Release: 1%{?_dist}
Epoch: 7
License: GPL
Group: System Environment/Daemons
Source: http://www.squid-cache.org/Squid/Versions/v2/2.7/squid-%{version}.tar.bz2
Source1: http://www.squid-cache.org/Squid/FAQ/FAQ.sgml
Source2: squid.init
Source3: squid.logrotate
Source4: squid.sysconfig
Source5: squid.pam
Source6: squid-reverse.conf
Source98: perl-requires-squid.sh

# Upstream patches

# External patches

# Local patches
# Applying upstream patches first makes it less likely that local patches
# will break upstream ones.
Patch201: squid-2.5.STABLE11-config.patch
Patch202: squid-2.5.STABLE4-location.patch
Patch203: squid-2.6.STABLE2-build.patch
Patch204: squid-2.5.STABLE4-perlpath.patch
Patch205: squid-2.5.STABLE12-smb-path.patch

# awie patch > 300
Patch300: squid-2.7.STABLE9-cache.patch
Patch301: squid-2.7.STABLE9-pidfile.patch
Patch302: squid-2.7.STABLE9-errorpage.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: bash >= 2.0
Requires(pre): /sbin/chkconfig logrotate shadow-utils
Requires(post): chkconfig, grep
Requires(postun): grep, sed
BuildRequires: openjade linuxdoc-tools openldap-devel pam-devel openssl-devel
Obsoletes: squid-novm

%description
Squid is a high-performance proxy caching server for Web clients,
supporting FTP, gopher, and HTTP data objects. Unlike traditional
caching software, Squid handles all requests in a single,
non-blocking, I/O-driven process. Squid keeps meta data and especially
hot objects cached in RAM, caches DNS lookups, supports non-blocking
DNS lookups, and implements negative caching of failed requests.

Squid consists of a main server program squid, a Domain Name System
lookup program (dnsserver), a program for retrieving FTP data
(ftpget), and some management and client tools.

%prep
%setup -q

%patch201 -p1 -b .config
%patch202 -p1 -b .location
%patch203 -p1 -b .build
%patch204 -p1 -b .perlpath
%patch205 -p1 -b .smb
%patch300 -p1 -b .cache
%patch301 -p1 -b .pidfile
%patch302 -p1 -b .errorpage

%build
export CFLAGS="-fPIE -Os -g -pipe -fsigned-char %{optflags}" ; export LDFLAGS="-pie" ;
%configure \
   --exec_prefix=/usr \
   --bindir=%{_sbindir} \
   --libexecdir=%{_libdir}/squid \
   --localstatedir=/var \
   --datadir=%{_datadir} \
   --sysconfdir=/etc/squid \
   --enable-default-err-language="English" \
   --enable-err-languages="English" \
   --enable-epoll \
   --enable-snmp \
   --enable-removal-policies="heap,lru" \
   --enable-storeio="aufs,coss,diskd,null,ufs" \
   --enable-ssl \
   --with-openssl=/usr/kerberos \
   --enable-delay-pools \
   --enable-linux-netfilter \
   --with-pthreads \
   --enable-ntlm-auth-helpers="SMB,fakeauth" \
   --enable-external-acl-helpers="ip_user,ldap_group,unix_group,wbinfo_group" \
   --enable-auth="basic,digest,ntlm,negotiate" \
   --enable-digest-auth-helpers="password" \
   --enable-useragent-log \
   --enable-referer-log \
   --disable-dependency-tracking \
   --enable-cachemgr-hostname=localhost \
   --enable-basic-auth-helpers="LDAP,MSNT,NCSA,PAM,SMB,YP,getpwnam,multi-domain-NTLM,SASL" \
   --enable-negotiate-auth-helpers="squid_kerb_auth" \
   --enable-cache-digests \
   --enable-ident-lookups \
   %ifnarch ppc64 ia64 x86_64 s390x
   --with-large-files \
   %endif
   --enable-follow-x-forwarded-for \
   --enable-wccpv2 \
   --with-maxfd=16384 \
   --enable-kill-parent-hack


export CFLAGS="-fPIE -Os -g -pipe -fsigned-char" ; export LDFLAGS=-pie ;
make %{?_smp_mflags}

mkdir faq
cp %{SOURCE1} faq
cd faq
sgml2html FAQ.sgml

#cd ..

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall  \
	sysconfdir=$RPM_BUILD_ROOT/etc/squid \
	localstatedir=$RPM_BUILD_ROOT/var \
	bindir=$RPM_BUILD_ROOT/%{_sbindir} \
	libexecdir=$RPM_BUILD_ROOT/%{_libdir}/squid

ln -s %{_datadir}/squid/errors/English $RPM_BUILD_ROOT/etc/squid/errors
ln -s %{_datadir}/squid/icons $RPM_BUILD_ROOT/etc/squid/icons

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
mkdir -p $RPM_BUILD_ROOT/etc/squid

install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/squid
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/squid
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/squid
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/squid
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/etc/squid/squid-reverse.conf

mkdir -p $RPM_BUILD_ROOT/var/log/squid
mkdir -p $RPM_BUILD_ROOT/var/spool/squid

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ncsa_auth.8 # shipped with man-pages, so we don't want to have a conflict
rm -f $RPM_BUILD_ROOT%{_sbindir}/{RunAccel,RunCache}
rm -f $RPM_BUILD_ROOT/squid.httpd.tmp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc faq/* README ChangeLog QUICKSTART doc/*
%doc contrib/url-normalizer.pl contrib/rredir.* contrib/user-agents.pl

%attr(755,root,root) %dir /etc/squid
%attr(755,root,root) %dir %{_libdir}/squid
%attr(750,squid,squid) %dir /var/log/squid
%attr(750,squid,squid) %dir /var/spool/squid
%attr(644,root,root) /etc/pam.d/squid
%attr(4750,root,squid) %{_libdir}/squid/ncsa_auth
%attr(4750,root,squid) %{_libdir}/squid/pam_auth
%attr(755,root,root) %{_sbindir}/cossdump

%config(noreplace) %attr(640,root,squid) /etc/squid/squid.conf
%config(noreplace) %attr(644,root,squid) /etc/squid/cachemgr.conf
%config(noreplace) /etc/squid/mime.conf
%config(noreplace) /etc/sysconfig/squid
%config(noreplace) /etc/squid/msntauth.conf
%config(noreplace) /etc/squid/mib.txt
%config(noreplace) %attr(640,root,squid) /etc/squid/squid-reverse.conf
/etc/squid/msntauth.conf.default
/etc/squid/squid.conf.default
/etc/squid/mime.conf.default

%config(noreplace) /etc/squid/errors
%config(noreplace) %{_datadir}/squid/errors
%config(noreplace) /etc/squid/icons
%config(noreplace) /etc/rc.d/init.d/squid
%config(noreplace) /etc/logrotate.d/squid
%{_datadir}/squid/icons
%{_sbindir}/squid
%{_sbindir}/squidclient
%{_mandir}/man8/*
%{_libdir}/squid/*

%pre
if ! getent group squid >/dev/null 2>&1; then
  /usr/sbin/groupadd -g 23 squid
fi

if ! getent passwd squid >/dev/null 2>&1 ; then
  /usr/sbin/useradd -g 23 -u 23 -d /var/spool/squid -r -s /sbin/nologin squid >/dev/null 2>&1 || exit 1 
fi

for i in /var/log/squid /var/spool/squid ; do
	if [ -d $i ] ; then
		for adir in `find $i -maxdepth 0 \! -user squid`; do
			chown -R squid:squid $adir
		done
	fi
done

exit 0

%post
/sbin/chkconfig --add squid
ln -snf %{_datadir}/squid/errors/English /etc/squid/errors

%preun
if [ $1 = 0 ] ; then
	service squid stop >/dev/null 2>&1
	rm -f /var/log/squid/*
	/sbin/chkconfig --del squid
fi

%postun
if [ "$1" -ge "1" ] ; then
	service squid condrestart >/dev/null 2>&1
fi

%triggerin -- samba-common
/usr/sbin/usermod -a -G winbind squid >/dev/null 2>&1 || \
    chgrp squid /var/cache/samba/winbindd_privileged >/dev/null 2>&1 || :

%changelog
* Thu Dec 14 2011 nawawi jamili <nawawi@rutweb.com>
- Initial rutweb version

* Tue May 11 2010 nawawi <mohd.nawawi@gmail.com> - 7:2.7.STABLE9-1
- update to the latest upstream

* Fri Mar 12 2010 nawawi <mohd.nawawi@gmail.com> - 7:2.7.STABLE8-1
- update to the latest upstream
