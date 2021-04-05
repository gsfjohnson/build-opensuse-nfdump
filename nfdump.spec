
%global _hardened_build		1

%define nfdumpuser	nobody
%define nfdumpgroup	nobody
%define nfcapddatadir	/var/lib/nfcapd
%define sfcapddatadir	/var/lib/sfcapd

Summary: NetFlow collecting and processing tools
Name: nfdump
Version: 1.6.22
Release: 1%{?dist}
License: GPLv2+ and BSD
Group: Applications/System
URL: https://github.com/phaag/nfdump

Source0: https://github.com/phaag/%{name}/archive/nfdump-%{version}.tar.bz2
#Source1: rc.nfcapd
#Source2: sysconfig.nfcapd
#Source3: rc.sfcapd
#Source4: sysconfig.sfcapd

BuildRequires:	autoconf
BuildRequires:	byacc
BuildRequires:	bzip2-devel
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	libpcap-devel
BuildRequires:	make
#BuildRequires:	rrdtool-devel
BuildRequires:	sed

Requires: nfdump-libs = %{version}-%{release}


%description
Nfdump is a set of tools to collect and process NetFlow data. It's fast and has
a powerful filter pcap like syntax. It supports NetFlow versions v1, v5, v7, v9
and IPFIX as well as a limited set of sflow. It includes support for CISCO ASA
(NSEL) and CISCO NAT (NEL) devices which export event logging records as v9
flows. Nfdump is fully IPv6 compatible.

%package libs
Summary:	Libraries used by NFDUMP packages
Group:		Applications/System

%description libs
Contains libraries used by NFDUMP utilities


%prep
%setup -q
#%{__cp} %{S:1} rc.nfcapd
#%{__cp} %{S:2} sysconfig.nfcapd
#%{__cp} %{S:3} rc.sfcapd
#%{__cp} %{S:4} sysconfig.sfcapd
#%{__perl} -pi -e '
#	s|\@NFDUMPUSER\@|%{nfdumpuser}|g;
#	s|\@NFDUMPGROUP\@|%{nfdumpgroup}|g;
#	s|\@NFCAPDDATADIR\@|%{nfcapddatadir}|g;
#	s|\@SFCAPDDATADIR\@|%{sfcapddatadir}|g;
#	' sysconfig.nfcapd sysconfig.sfcapd

%build
./autogen.sh
%configure \
    --enable-nsel \
    --enable-nfprofile \
    --enable-nftrack \
    --enable-sflow \
    --enable-readpcap \
    --enable-nfpcapd \
    --enable-shared \
    --disable-static

# removing rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# disable parallel build to get proper linking order
make

%install
make install DESTDIR=%{buildroot}
chmod 0644 AUTHORS ChangeLog README.md
rm -f %{buildroot}%{_libdir}/*.la

%{__install} -d %{buildroot}%{_sbindir}/
%{__mv} %{buildroot}%{_bindir}/?fcapd %{buildroot}%{_sbindir}/

#%{__install} -D rc.nfcapd %{buildroot}/etc/init.d/nfcapd
#%{__install} -D rc.sfcapd %{buildroot}/etc/init.d/sfcapd
##%{__ln_s} /etc/init.d/nfcapd %{buildroot}%{_sbindir}/rcnfcapd
##%{__ln_s} /etc/init.d/sfcapd %{buildroot}%{_sbindir}/rcsfcapd
#%{__install} -D sysconfig.nfcapd %{buildroot}/var/adm/fillup-templates/sysconfig.nfcapd
#%{__install} -D sysconfig.sfcapd %{buildroot}/var/adm/fillup-templates/sysconfig.sfcapd


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
#%license LICENSE
%defattr(0644, root, root, 0755)
%doc AUTHORS ChangeLog INSTALL README.md
%doc %{_mandir}/man?/*
/var/adm/fillup-templates/*

%defattr(-, root, root)
%{_bindir}/*
%{_sbindir}/*

/etc/init.d/?fcapd

%files libs
%{_libdir}/libnfdump-%{version}.so
%{_libdir}/libnfdump.so


%changelog
* Wed Jun 29 2016 Denis Fateyev <denis@fateyev.com> - 1.6.15-2
- Remove extra debug output option

* Sat Jun 11 2016 Denis Fateyev <denis@fateyev.com> - 1.6.15-1
- Update to version 1.6.15

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Denis Fateyev <denis@fateyev.com> - 1.6.13-1
- Update to version 1.6.13

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 03 2014 Denis Fateyev <denis@fateyev.com> - 1.6.12-1
- Update to version 1.6.12

* Wed Feb 05 2014 Denis Fateyev <denis@fateyev.com> - 1.6.11-1
- Initial Fedora RPM release
